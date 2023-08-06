# StatusValue 배열을 정의합니다 (전역 변수로 가정합니다)
StatusValue = [0] * 8

def hyGs_RecvByte(b):
    global sRecvMode
    global cRecvCmd
    global StatusValue

    # 정적 변수를 초기화합니다
    if 'sRecvMode' not in globals():
        sRecvMode = 0

    if 'cRecvCmd' not in globals():
        cRecvCmd = [0, 0, 0, 0]

    # 56 00 ....
    if sRecvMode == 0x00:
        sRecvMode = 0x01 if b == 0x56 else 0

    elif sRecvMode == 0x01:
        sRecvMode = 0x02 if b == 0x00 else (1 if b == 0x56 else 0)

    elif sRecvMode == 0x02:
        sRecvMode = 0x10 if b == 0x48 else (1 if b == 0x56 else 0)

    elif sRecvMode == 0x10:
        sRecvMode = sRecvMode + 1 if b == 0x00 else (1 if b == 0x56 else 0)

    elif sRecvMode == 0x11:
        sRecvMode += 1
        cRecvCmd[0] = b

    elif sRecvMode == 0x12:
        sRecvMode += 1
        cRecvCmd[1] = b

    elif sRecvMode == 0x13:
        sRecvMode = 0
        cRecvCmd[2] = b
        if 64 <= cRecvCmd[0] < 64 + 8:  # 8비트 데이터 값일 때
            if (cRecvCmd[0] ^ cRecvCmd[1]) == cRecvCmd[2]:  # XOR
                StatusValue[cRecvCmd[0] - 64] = cRecvCmd[1]

    else:
        sRecvMode = 1 if b == 0x56 else 0

# 예제 사용:
if __name__ == "__main__":
    # 수신한 바이트들을 시뮬레이션합니다
    received_bytes = [0x56, 0x00, 0x48, 0x00, 0x65, 0x15, 0x79]

    for byte in received_bytes:
        hyGs_RecvByte(byte)

    # StatusValue 배열을 출력합니다
    print(StatusValue)
