import struct
import numpy as np
from typing import Tuple, Optional
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
#%%


def __poi_converter(poi: Tuple[int, int], _samples) -> Tuple[Tuple[int, int], int]:
    """POI의 범위를 검사하고 반환해주는 함수

    :param poi: (시작, 끝)으로 이루어진 poi 범위
    :param _samples: 파형의 실제 샘플수
    :return: (poi, poi_len)
    """
    if poi is None: _trunc_range = (0, _samples - 1)  # 0 ~ 25002-1
    else: _trunc_range = (poi[0], poi[1])  # 1 ~ 25002

    _trunc_len = _trunc_range[1] - _trunc_range[0] + 1

    if _trunc_range[0] < 0 or _trunc_range[1] > _samples - 1 or _trunc_len <= 0:
        raise RuntimeError("\nPOI error. All: poi=None, else: (a, b). a>=0, b<=SAMPLES")

    return _trunc_range, _trunc_len
    pass


def convert_btr_2_npy(poi: Optional[Tuple[int, int]], import_file_path: str, traces_path_exp: Optional[str] = None) -> np.ndarray:
    """Binary traces(.btr) 파일을 numpy.ndarray 의 직렬화된 파일로 저장하는 함수

    :param poi: 일부만 추출할 경우 인자 전달. 전체 파형을 추출할 경우 None 전달
    :param import_file_path: .btr 파일의 위치 (경로 + 파일명)
    :param traces_path_exp:  변환된 numpy.ndarray 객체 파일이 저장될 위치 (경로 + 파일명). 확장자는 .npy로 한다.
    :return: numpy array로 변환된 파형 데이터
    """
    print('Binary Traces file. (.btr)')
    print('-' * 50)
    _fp = open(import_file_path, 'rb')

    _trace_num = struct.unpack('i', _fp.read(4))[0]  # num of traces
    _trace_sample = struct.unpack('i', _fp.read(4))[0]  # samples

    _trunc_range, _trunc_len = __poi_converter(poi, _trace_sample)

    _traces = np.empty(shape=(_trace_num, _trunc_len))

    for _i in range(_trace_num):
        __trace_index = struct.unpack('i', _fp.read(4))[0]
        _traces[_i] = struct.unpack(str(_trace_sample) + 'f', _fp.read(_trace_sample * 4))[_trunc_range[0]: _trunc_range[1] + 1]
        print(f'\r* Trace-{__trace_index + 1}', ' read', end='', flush=True)

    _fp.close()
    print()
    print('-' * 50)

    if traces_path_exp is not None:
        np.save(traces_path_exp, _traces)
        print(f'Traces - {traces_path_exp} saved.')

    return _traces
    pass


def show_mean_trace_btr(import_file_path: str, poi: Optional[Tuple[int, int]] = None) -> (np.ndarray, plt.Figure):
    """Binary traces(.btr) 파일로 이루어진 파형의 평균을 시각화 하는 함수

    :param import_file_path: Binary traces(.btr) 파일의 위치 (경로 + 파일명)
    :param poi: 일부만 평균을 내어 볼 경우 인자 전달
    :return: (평균파형, figure)
    """
    _fp_btr = open(import_file_path, 'rb')

    _trace_num = struct.unpack('i', _fp_btr.read(4))[0]  # num of traces
    _trace_sample = struct.unpack('i', _fp_btr.read(4))[0]  # samples

    _trunc_range, _trunc_len = __poi_converter(poi, _trace_sample)

    _traces = np.zeros(shape=(_trunc_len, ))

    for _i in range(_trace_num):
        __trace_index = struct.unpack('i', _fp_btr.read(4))[0]
        __tmp_traces = struct.unpack(str(_trace_sample) + 'f', _fp_btr.read(_trace_sample * 4))[_trunc_range[0]: _trunc_range[1] + 1]
        _traces += __tmp_traces
        print(f'\r* Trace-{__trace_index + 1}', ' accumulated -', end='', flush=True)

    _mean_traces = _traces/_trace_num

    _mean_fig: plt.Figure = plt.figure(figsize=(16, 9))
    _mean_axe: plt.Axes = _mean_fig.add_subplot(1, 1, 1)
    _mean_axe.plot(range(_trunc_range[0], _trunc_range[1] + 1), _mean_traces)
    _mean_fig.show()
    _fp_btr.close()
    return _mean_traces, _mean_fig
    pass


def convert_hex_data_2_npy(import_file_path: str, export_file_path: Optional[str] = None) -> np.ndarray:
    """16진수 문자열로 구성된 평문/암호문 파일을 읽어 numpy.ndarray 의 직렬화된 파일로 저장하는 함수

    :param import_file_path: 평문/암호문의 16진수 문자열이 나열된 텍스트 파일 위치 (경로 + 파일명)
    :param export_file_path: numpy.ndarray로 변환되어 저장될 파일의 위치 (경로 + 파일명). 확장자는 .npy로 한다.
    :return: numpy array로 변환된 데이터
    """
    _fp = open(import_file_path, 'r')
    _data = _fp.readlines()
    for i in range(len(_data)):
        _data[i] = _data[i].replace(" ", "").replace("\n", "")

    _data = np.array(_data)

    if export_file_path is not None:
        np.save(export_file_path, _data)

    return _data
    pass
