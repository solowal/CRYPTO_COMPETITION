from pub_data_handler import convert_btr_2_npy, convert_hex_data_2_npy, show_mean_trace_btr
#%%

#파일을 읽기 전에 전체 구조를 파악하여 부분적으로 읽어들일 수 있도록 평균 파형을 보여주는 함수
show_mean_trace_btr("../data/STM-AES.btr",  # 읽어들일 btr 파일
                    (0,60000)) # 읽어올 파형의 샘플 인덱스. 전체를 읽을경우 None, 혹은 생략 가능.

# btr 파일을 읽어 numpy ndarray로 만드는 함수
traces = convert_btr_2_npy((0,100),  # 읽어들일 파형의 샘플 인덱스 입니다. 전체를 읽을 경우 None을 전달합니다.
                           "../data/STM-AES.btr",  # btr 파일의 경로입니다.
                           "../npy/stm-aes-traces.npy")  # numpy.ndarray 형태로 변환된 객체를 저장하려면 위치 및 파일 명을 입력하고
                                            # 저장하지 않으려면 None을 전달하거나 생략하면 됩니다.

# 16진수 문자열로이루어진 텍스트파일을 읽는 함수
plain = convert_hex_data_2_npy("../data/STM-AES-plain.txt",  # 16진수 문자열로 이루어진 txt 파일
                               "../npy/stm-aes-plain.npy")  # 변환된 객체를 파일로 저장하려면 경로 및 파일명 입력. 생략 가능.

cipher = convert_hex_data_2_npy("../data/STM-AES-cipher.txt",  # 16진수 문자열로 이루어진 txt 파일
                                "../npy/stm-aes-cipher.npy")  # 변환된 객체를 파일로 저장하려면 경로 및 파일명 입력. 생략 가능.

keys = convert_hex_data_2_npy("../data/STM-AES-key.txt",  # 16진수 문자열로 이루어진 txt 파일
                              "../npy/stm-aes-keys.npy")  # 변환된 객체를 파일로 저장하려면 경로 및 파일명 입력. 생략 가능.

