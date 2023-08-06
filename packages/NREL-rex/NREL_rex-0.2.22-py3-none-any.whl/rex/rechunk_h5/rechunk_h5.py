"""
Module to rechunk existing .h5 files
"""
import h5py
import logging
import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
import time
from warnings import warn

logger = logging.getLogger(__name__)


def get_dataset_attributes(h5_file, out_json=None):
    """
    Extact attributes, dtype, and chunk size for all datasets in .h5 file

    Parameters
    ----------
    h5_file : str
        Path to source h5 file to scrape dataset data from
    out_json : str, optional
        Path to output json to save DataFrame of dataset attributes to,
        by default None

    Returns
    -------
    ds_attrs : pandas.DataFrame
        Attributes (attrs, dtype, chunks) for all datasets in source .h5 file
    """
    attrs_list = []
    with h5py.File(h5_file, 'r') as f:
        datasets = list(f)
        for ds_name in datasets:
            ds = f[ds_name]
            try:
                attrs = dict(ds.attrs)
                if not attrs:
                    attrs = None

                ds_attrs = {'attrs': attrs,
                            'dtype': ds.dtype.name,
                            'chunks': ds.chunks}
                ds_attrs = pd.Series(ds_attrs)
                ds_attrs.name = ds_name
                attrs_list.append(ds_attrs.to_frame().T)
            except Exception:
                pass

    ds_attrs = pd.concat(attrs_list)
    if out_json is not None:
        ds_attrs.to_json(out_json)

    return ds_attrs


def get_chunk_slices(ds_dim, chunk_size):
    """
    Create list of chunk slices [(s_i, e_i), ...]

    Parameters
    ----------
    ds_len : int
        Length of dataset axis to chunk
    chunk_size : int
        Size of chunks

    Returns
    -------
    chunks : list
        List of chunk start and end positions
        [(s_i, e_i), (s_i+1, e_i+1), ...]
    """
    chunks = list(range(0, ds_dim, chunk_size))
    if chunks[-1] < ds_dim:
        chunks.append(ds_dim)
    else:
        chunks[-1] = ds_dim

    chunks = list(zip(chunks[:-1], chunks[1:]))

    return chunks


def get_dtype(col):
    """
    Get column dtype for converstion to records array

    Parameters
    ----------
    col : pandas.Series
        Column from pandas DataFrame

    Returns
    -------
    out : str
        String representation of converted dtype for column:
        -  float = float32
        -  int = int16 or int32 depending on data range
        -  object/str = U* max length of strings in col
    """
    dtype = col.dtype

    if isinstance(dtype, CategoricalDtype):
        col = col.astype(type(col.values[0]))
        out = get_dtype(col)
    elif np.issubdtype(dtype, np.floating):
        out = 'float32'
    elif np.issubdtype(dtype, np.integer):
        if col.max() < 32767:
            out = 'int16'
        else:
            out = 'int32'
    elif np.issubdtype(dtype, np.object_):
        size = int(col.astype(str).str.len().max())
        out = 'S{:}'.format(size)
    else:
        out = dtype

    return out


def to_records_array(df):
    """
    Convert pandas DataFrame to numpy Records Array

    Parameters
    ----------
    df : pandas.DataFrame
        Pandas DataFrame to be converted

    Returns
    -------
    numpy.rec.array
        Records array of input df
    """
    meta_arrays = []
    dtypes = []
    for c_name, c_data in df.iteritems():
        dtype = get_dtype(c_data)

        if np.issubdtype(dtype, np.bytes_):
            data = c_data.astype(str).str.encode('utf-8').values
        else:
            data = c_data.values

        arr = np.array(data, dtype=dtype)
        meta_arrays.append(arr)
        dtypes.append((c_name, dtype))

    return np.core.records.fromarrays(meta_arrays, dtype=dtypes)


class RechunkH5:
    """
    Class to create new .h5 file with new chunking
    """
    def __init__(self, h5_src, h5_dst, version=None):
        """
        Initalize class object

        Parameters
        ----------
        h5_src : str
            Source .h5 file path
        h5_dst : str
            Destination path for rechunked .h5 file
        version : str
            File version number
        """
        self._src_path = h5_src
        self._src_dsets = None
        self._dst_path = h5_dst
        self._dst_h5 = h5py.File(h5_dst, 'w')
        if version:
            self._dst_h5.attrs['version'] = version

        self._time_slice = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

        if type is not None:
            raise

    def close(self):
        """
        Close h5 instance
        """
        self._dst_h5.close()

    @property
    def src_dsets(self):
        """
        Available dsets in source .h5

        Returns
        -------
        list
        """
        if self._src_dsets is None:
            with h5py.File(self._src_path, mode='r') as f:
                self._src_dsets = list(f)

        return self._src_dsets

    @property
    def dsets(self):
        """
        Datasets available in h5_file

        Returns
        -------
        list
            List of datasets in h5_file
        """
        return list(self._dst_h5)

    @property
    def time_slice(self):
        """
        Time slice or mask to use for rechunking temporal access

        Returns
        -------
        slice
        """
        return self._time_slice

    @staticmethod
    def _check_dtype(ds_in, dset_attrs):
        """
        Check dataset dtype against source dataset dtype

        Parameters
        ----------
        ds_in : h5py.Dataset
            Source h5 Dataset
        dset_attrs : dict
            Dictionary of dataset attributes (dtype, chunk, attrs)
        """
        dtype = dset_attrs['dtype']
        attrs = dset_attrs['attrs']
        if ds_in.dtype.name != dtype:
            msg = ('Source dtype ({}) does not match specified dtype ({}), '
                   .format(ds_in.dtype, dtype))
            logger.warning(msg)
            warn(msg)
            float_to_int = (np.issubdtype(ds_in.dtype, np.floating)
                            and np.issubdtype(dtype, np.integer))
            int_to_float = (np.issubdtype(ds_in.dtype, np.integer)
                            and np.issubdtype(dtype, np.floating))
            if float_to_int:
                if not any(c for c in attrs if 'scale_factor' in c):
                    msg = ('Cannot downscale from {} to {} without a '
                           'scale_factor!'.format(ds_in.dtype, dtype))
                    logger.error(msg)
                    raise RuntimeError(msg)
                else:
                    msg = 'Converting {} to {}'.format(ds_in.dtype, dtype)
                    logger.warning(msg)
                    warn(msg)
            elif int_to_float:
                msg = ('Cannot scale up an {} to a {}'
                       .format(ds_in.dtype, dtype))
                logger.error(msg)
                raise RuntimeError(msg)
            elif not np.issubdtype(dtype, ds_in.dtype):
                msg = ('Output dtype ({}) has greater precision than input '
                       'dtype ({}), using input dtype'
                       .format(dtype, ds_in.dtype))
                logger.warning(msg)
                warn(msg)

                dset_attrs['dtype'] = ds_in.dtype

        return dset_attrs

    @staticmethod
    def _check_attrs(ds_in, dset_attrs):
        """
        Check dataset attributes against source dataset attributes

        Parameters
        ----------
        ds_in : h5py.Dataset
            Source h5 Dataset
        dset_attrs : dict
            Dictionary of dataset attributes (dtype, chunk, attrs)
        """
        attrs = dset_attrs['attrs']
        for key, value in attrs.items():
            src_value = ds_in.attrs.get(key)
            if src_value:
                if isinstance(src_value, bytes):
                    src_value = src_value.decode('utf-8')

                if src_value != value:
                    msg = ('Attr {} value ({}) does not match '
                           'source value ({}), using source value.'
                           .format(key, value, src_value))
                    logger.warning(msg)
                    warn(msg)

                    dset_attrs['attrs'][key] = src_value

        return dset_attrs

    @staticmethod
    def check_dset_attrs(ds_in, dset_attrs, check_attrs=False):
        """
        Check dataset attributes (dtype, scale_factor, units) against source
        Dataset

        Parameters
        ----------
        ds_in : h5py.Dataset
            Source h5 Dataset
        dset_attrs : dict
            Dictionary of dataset attributes (dtype, chunk, attrs)
        check_attrs : bool, optional
            Flag to compare source and specified dataset attributes,
            by default False
        """
        dset_attrs = RechunkH5._check_dtype(ds_in, dset_attrs)

        if check_attrs:
            dset_attrs = RechunkH5._check_attrs(ds_in, dset_attrs)

        return dset_attrs

    @staticmethod
    def _check_data(data, dset_attrs):
        """
        Check data dtype and scale if needed

        Parameters
        ----------
        data : ndarray
            Data to be written to disc
        dtype : str
            dtype of data on disc
        scale_factor : int
            Scale factor to scale data to integer (if needed)

        Returns
        -------
        data : ndarray
            Data ready for writing to disc:
            - Scaled and converted to dtype
        """
        dtype = dset_attrs['dtype']
        float_to_int = (np.issubdtype(dtype, np.integer)
                        and np.issubdtype(data.dtype, np.floating))
        if float_to_int:
            attrs = dset_attrs['attrs']
            scale_factor = [c for c in attrs if 'scale_factor' in c][0]
            scale_factor = attrs[scale_factor]

            # apply scale factor and dtype
            data = np.multiply(data, scale_factor)
            if np.issubdtype(dtype, np.integer):
                data = np.round(data)

            data = data.astype(dtype)

        return data

    def init_dset(self, dset_name, dset_shape, dset_attrs):
        """
        Create dataset and add attributes and load data if needed

        Parameters
        ----------
        dset_name : str
            Dataset name to be created
        dset_shape : tuple
            Dataset shape
        dset_attrs : dict
            Dictionary of dataset attributes (dtype, chunks, attrs, name)

        Returns
        -------
        ds : h5py.Dataset
            Initalized h5py Dataset instance
        """
        dtype = dset_attrs['dtype']
        chunks = dset_attrs['chunks']
        attrs = dset_attrs['attrs']
        name = dset_attrs.get('name', None)
        if name is not None:
            dset_name = name

        if chunks:
            chunks = tuple(chunks)

        logger.debug('Creating {} with shape: {}, dtype: {}, chunks: {}'
                     .format(dset_name, dset_shape, dtype, chunks))
        ds = self._dst_h5.create_dataset(dset_name, shape=dset_shape,
                                         dtype=dtype, chunks=chunks)
        if attrs:
            for attr, value in attrs.items():
                if attr not in ['freq', 'start']:
                    ds.attrs[attr] = value

        logger.info('- {} initialized'.format(dset_name))

        return ds

    def load_time_index(self, attrs, resolution=None):
        """
        Transfer time_index to rechunked .h5

        Parameters
        ----------
        attrs : pandas.Series
            Dataset attributes associated with time_index
        resolution : str, optional
            New time resolution, by default None
        """
        ts = time.time()
        logger.info('Rechunking time_index')
        with h5py.File(self._src_path, 'r') as f:
            time_index = f['time_index'][...]

        timezone = attrs['attrs'].get('timezone', None)
        if timezone is not None or resolution is not None:
            time_index = pd.to_datetime(time_index.astype(str))
            if timezone is not None:
                if time_index.tz is not None:
                    time_index = time_index.tz_convert(timezone)
                else:
                    time_index = time_index.tz_localize(timezone)

            if resolution is not None:
                resample = pd.date_range(time_index.min(), time_index.max(),
                                         freq=resolution)
                if len(resample) > len(time_index):
                    msg = ("Resolution ({}) must be > time_index resolution "
                           "({})".format(resolution, time_index.freq))
                    logger.error(msg)
                    raise RuntimeError(msg)

                self._time_slice = time_index.isin(resample)
                time_index = time_index[self.time_slice]

            time_index = time_index.astype(str)
            dtype = 'S{}'.format(len(time_index[0]))
            time_index = np.array(time_index, dtype=dtype)

        attrs['dtype'] = time_index.dtype

        ds = self.init_dset('time_index', time_index.shape, attrs)
        ds[...] = time_index
        logger.info('- time_index transfered')
        tt = (time.time() - ts) / 60
        logger.debug('\t- {:.2f} minutes'.format(tt))

    def load_meta(self, attrs, meta_path=None):
        """
        Transfer meta data to rechunked .h5

        Parameters
        ----------
        attrs : pandas.Series
            Dataset attributes associated with meta
        """
        ts = time.time()
        logger.info('Rechunking meta')
        meta = None
        if meta_path is not None:
            if meta_path.endswith('.csv'):
                meta = pd.read_csv(meta_path)
                meta = to_records_array(meta)
            elif meta_path.endswith('.npy'):
                meta = np.load(meta_path)

        if meta is None:
            with h5py.File(self._src_path, 'r') as f:
                meta = f['meta'][...]

        if isinstance(attrs['chunks'], int):
            attrs['chunks'] = (attrs['chunks'], )

        attrs['dtype'] = meta.dtype
        ds = self.init_dset('meta', meta.shape, attrs)
        ds[...] = meta
        logger.info('- meta transfered')
        tt = (time.time() - ts) / 60
        logger.debug('\t- {:.2f} minutes'.format(tt))

    def load_coords(self, attrs):
        """
        Create coordinates and add to rechunked .h5

        Parameters
        ----------
        attrs : pandas.Series
            Dataset attributes associated with coordinates
        """
        ts = time.time()
        logger.info('Rechunking coordinates')
        meta_data = self._dst_h5['meta'][...]
        coords = np.dstack((meta_data['latitude'], meta_data['longitude']))[0]
        attrs['dtype'] = coords.dtype

        if isinstance(attrs['chunks'], int):
            attrs['chunks'] = (attrs['chunks'], 2)

        ds = self.init_dset('coordinates', coords.shape, attrs)
        ds[...] = coords
        logger.info('- coordinates transfered')
        tt = (time.time() - ts) / 60
        logger.debug('\t- {:.2f} minutes'.format(tt))

    def load_data(self, ds_in, ds_out, shape, dset_attrs, process_size=None,
                  data=None, reduce=False):
        """
        Load data from ds_in to ds_out

        Parameters
        ----------
        ds_in : h5py.Dataset
            Open dataset instance for source data
        ds_out : h5py.Dataset
            Open dataset instance for rechunked data
        shape : tuple
            Dataset shape
        dset_attrs : dict
            Dictionary of dataset attributes (dtype, chunks, attrs)
        process_size : int, optional
            Size of each chunk to be processed at a time, by default None
        data : ndarray, optional
            Data to load into ds_out, by default None
        reduce : bool, optional
            Reduce temporal resolution, by default False
        """
        if process_size is not None and data is None:
            by_rows = False
            chunks = ds_in.chunks
            if isinstance(chunks, tuple):
                sites = shape[1]
            else:
                by_rows = True
                sites = shape[0]

            slice_map = get_chunk_slices(sites, process_size)
            for s, e in slice_map:
                if by_rows:
                    ds_out[s:e] = self._check_data(ds_in[s:e], dset_attrs)
                else:
                    data = ds_in[:, s:e]
                    if reduce:
                        data = data[self.time_slice]

                    ds_out[:, s:e] = self._check_data(data, dset_attrs)

                logger.debug('\t- chunk {}:{} transfered'.format(s, e))
        else:
            if data is None:
                data = ds_in[:]
                if reduce:
                    data = data[self.time_slice]

                ds_out[:] = self._check_data(data, dset_attrs)
            else:
                ds_out[:] = self._check_data(data, dset_attrs)

    def load_dset(self, dset_name, dset_attrs, process_size=None,
                  check_attrs=False):
        """
        Transfer dataset from domain to combined .h5

        Parameters
        ----------
        dset_name : str
            Dataset to transfer
        dset_attrs : dict
            Dictionary of dataset attributes (dtype, chunks, attrs)
        process_size : int, optional
            Size of each chunk to be processed at a time, by default None
        check_attrs : bool, optional
            Flag to compare source and specified dataset attributes,
            by default False
        """
        if dset_name not in self._dst_h5:
            ts = time.time()
            logger.info('Rechunking {}'.format(dset_name))
            with h5py.File(self._src_path, 'r') as f_in:
                ds_in = f_in[dset_name]
                shape = ds_in.shape
                data = None
                if shape[0] == 1:
                    shape = (shape[1], )
                    data = ds_in[0]
                    logger.debug('\t- Reduce Dataset shape to {}'
                                 .format(shape))

                reduce = (self.time_slice is not None
                          and len(self.time_slice) == shape[0])
                if reduce:
                    shape = (self.time_slice.sum(), shape[1])

                dset_attrs = self.check_dset_attrs(ds_in, dset_attrs,
                                                   check_attrs=check_attrs)
                ds_out = self.init_dset(dset_name, shape, dset_attrs)

                self.load_data(ds_in, ds_out, shape, dset_attrs,
                               process_size=process_size, data=data,
                               reduce=reduce)

            logger.info('- {} transfered'.format(dset_name))
            tt = (time.time() - ts) / 60
            logger.debug('\t- {:.2f} minutes'.format(tt))
        else:
            logger.warning('{} already exists in {}'
                           .format(dset_name, self._dst_path))

    @staticmethod
    def pop_dset_attrs(var_attrs, dset):
        """
        Pop attributres for given dataset from dataset attributes DataFrame

        Parameters
        ----------
        dset_attrs : pandas.DataFrame
            DataFrame of dataset attributes (dtype, chunks, attrs)
        dset : str
            Dataset of interest

        Returns
        -------
        dset_attrs : pandas.DataFrame
            Updated DataFrame of dataset attributes (dtype, chunks, attrs)
        attrs : pandas.Series
            Series of attributes for given dataset
        """
        attrs = var_attrs.loc[dset]
        var_attrs = var_attrs.drop(dset)

        return var_attrs, attrs

    @staticmethod
    def _parse_var_attrs(var_attrs):
        """
        Parse variable attributes from file if needed

        Parameters
        ----------
        var_attrs : str | pandas.DataFrame
            DataFrame of variable attributes or .json containing variable
            attributes

        Returns
        -------
        var_attrs : pandas.DataFrame
            DataFrame mapping variable (dataset) name to .h5 attributes
        """
        if isinstance(var_attrs, str):
            var_attrs = pd.read_json(var_attrs)
        elif not isinstance(var_attrs, pd.DataFrame):
            msg = ("Variable attributes are expected as a .json file or a "
                   "pandas DataFrame, but a {} was provided!"
                   .format(type(var_attrs)))
            logger.error(msg)
            raise TypeError(msg)

        var_attrs = var_attrs.where(var_attrs.notnull(), None)

        return var_attrs

    def rechunk(self, var_attrs, meta=None, process_size=None,
                check_dset_attrs=False, resolution=None):
        """
        Rechunk all variables in given variable attributes json

        Parameters
        ----------
        var_attrs : str | pandas.DataFrame
            DataFrame of variable attributes or .json containing variable
            attributes
        meta : str
            Path to .csv or .npy file containing meta to load into
            rechunked .h5 file
        process_size : int
            Size of each chunk to be processed at a time
        check_dset_attrs : bool, optional
            Flag to compare source and specified dataset attributes,
            by default False
        resolution : str, optional
            New time resolution, by default None
        """
        try:
            ts = time.time()
            with h5py.File(self._src_path, 'r') as f_in:
                for k, v in f_in.attrs.items():
                    logger.debug('Transfering global attribute {}'
                                 .format(k))
                    self._dst_h5.attrs[k] = v

            var_attrs = self._parse_var_attrs(var_attrs)
            if 'global' in var_attrs.index:
                var_attrs, global_attrs = self.pop_dset_attrs(var_attrs,
                                                              'global')

                for k, v in global_attrs['attrs'].items():
                    self._dst_h5.attrs[k] = v

            # Process time_index
            if 'time_index' in var_attrs.index:
                var_attrs, time_index_attrs = self.pop_dset_attrs(var_attrs,
                                                                  'time_index')
                self.load_time_index(time_index_attrs,
                                     resolution=resolution)

            # Process meta
            if 'meta' in var_attrs.index:
                var_attrs, meta_attrs = self.pop_dset_attrs(var_attrs, 'meta')
                self.load_meta(meta_attrs, meta_path=meta)

            # Process coordinates
            if 'coordinates' in var_attrs.index:
                var_attrs, coords_attrs = self.pop_dset_attrs(var_attrs,
                                                              'coordinates')
                self.load_coords(coords_attrs)

            mask = var_attrs.index.isin(self.src_dsets)
            var_attrs = var_attrs.loc[mask]
            for dset_name, dset_attrs in var_attrs.iterrows():
                self.load_dset(dset_name, dset_attrs,
                               process_size=process_size,
                               check_attrs=check_dset_attrs)

            tt = (time.time() - ts) / 60
            logger.debug('\t- {:} created in {:.2f} minutes'
                         .format(self._dst_path, tt))
        except Exception:
            logger.exception('Error creating {:}'.format(self._dst_path))

    @classmethod
    def run(cls, h5_src, h5_dst, var_attrs, version=None, meta=None,
            process_size=None, check_dset_attrs=False, resolution=None):
        """
        Rechunk h5_src to h5_dst using given attributes

        Parameters
        ----------
        h5_src : str
            Source .h5 file path
        h5_dst : str
            Destination path for rechunked .h5 file
        var_attrs : str | pandas.DataFrame
            DataFrame of variable attributes or .json containing variable
            attributes
        version : str
            File version number
        meta : str
            Path to .csv or .npy file containing meta to load into
            rechunked .h5 file
        process_size : int
            Size of each chunk to be processed at a time
        check_dset_attrs : bool, optional
            Flag to compare source and specified dataset attributes,
            by default False
        resolution : str, optional
            New time resolution, by default None
        """
        logger.info('Rechunking {} to {} using chunks given in {}'
                    .format(h5_src, h5_dst, var_attrs))
        try:
            with cls(h5_src, h5_dst, version=version) as r:
                r.rechunk(var_attrs, meta=meta, process_size=process_size,
                          check_dset_attrs=check_dset_attrs,
                          resolution=resolution)

            logger.info('{} complete'.format(h5_dst))
        except Exception:
            logger.exception("Error rechunking {}".format(h5_src))
            raise
