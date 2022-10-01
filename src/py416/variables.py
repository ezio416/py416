'''
| Author:  Ezio416
| Created: 2022-08-06
| Updated: 2022-10-01

- A collection of useful variables
'''

# Seconds in _____ amount of time
SEC_M =   60         # minute ----------- 60s
SEC_H =   3_600      # hour ------------- 60m
SEC_D =   86_400     # ephemeris day ---- 24h
SEC_SD =  86_164     # sidereal day ----- 23h 56m 4s ------ 23.9345
SEC_W =   604_800    # week ------------- 7d
SEC_30D = 2_592_000  # 30 days ---------- 30d
SEC_Y =   31_536_000 # year ------------- 365d
SEC_TY =  31_556_926 # tropical year ---- 365d 5h 48m 46s - 365.2422
SEC_JY =  31_557_600 # Julian year ------ 365d 6h --------- 365.25
SEC_SY =  31_558_149 # sidereal year ---- 365d 6h 9m 9s --- 365.2564
SEC_AY =  31_558_433 # anomalistic year - 365d 6h 13m 53s - 365.2596

# 10^n seconds in _____ amount of time
# (days, hours, minutes, seconds)
SEC10_3 =  (0, 0, 16, 40)        # 1,000 ---------- 16m 40s
SEC10_4 =  (0, 2, 46, 40)        # 10,000 --------- 2h 46m 40s
SEC10_5 =  (1, 3, 46, 40)        # 100,000 -------- 1d 3h 46m 40s
SEC10_6 =  (11, 13, 46, 40)      # 1,000,000 ------ 11d 13h 46m 40s
SEC10_7 =  (115, 17, 46, 40)     # 10,000,000 ----- 115d 17h 46m 40s
SEC10_8 =  (1_157, 9, 46, 40)    # 100,000,000 ---- 1,157d 9h 46m 40s ---- 3jy 61d 6h
SEC10_9 =  (11_574, 1, 46, 40)   # 1,000,000,000 -- 11,574d 1h 46m 40s --- 31jy 251d 6h
SEC10_10 = (115_740, 17, 46, 40) # 10,000,000,000 - 115,740d 17h 46m 40s - 316jy 321d

# Unix time for FAT filesystem epoch
UNIX_EPOCH_FAT = 315_532_800

# Unix time to UTC
# (year, month, day, hour, minute, second)
U2U_EPOCH = (1970, 1, 1, 0, 0, 0)
U2U_1700M = (2023, 11, 14, 22, 13, 20)
U2U_2147M = (2038, 1, 19, 3, 14, 7)
U2U_EPOCH_FAT = (1980, 1, 1, 0, 0, 0)

# bytes in a __bibyte
BYTE_K = 1_024                             # kibibyte - KiB
BYTE_M = 1_048_576                         # mebibyte - MiB
BYTE_G = 1_073_741_824                     # gibibyte - GiB
BYTE_T = 1_099_511_627_776                 # tebibyte - TiB
BYTE_P = 1_125_899_906_842_624             # pebibyte - PiB
BYTE_E = 1_152_921_504_606_846_976         # exbibyte - EiB
BYTE_Z = 1_180_591_620_717_411_303_424     # zebibyte - ZiB
BYTE_Y = 1_208_925_819_614_629_174_706_176 # yobibyte - YiB
