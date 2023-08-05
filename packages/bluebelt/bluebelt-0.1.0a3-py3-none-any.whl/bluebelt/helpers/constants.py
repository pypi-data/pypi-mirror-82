import math

def d2(N):
    # d2(N) is the expected value of the range of N observations from a normal population with standard deviation = 1.
    # Thus, if r is the range of a sample of N observations from a normal distribution with standard deviation = σ, then E(r) = d2(N)σ.

    d2_values = {2: 1.128, 3: 1.693, 4: 2.059, 5: 2.326, 6: 2.534, 7: 2.704, 8: 2.847, 9: 2.97, 10: 3.078, 11: 3.173, 12: 3.258, 13: 3.336, 14: 3.407, 15: 3.472, 16: 3.532, 17: 3.588, 18: 3.64, 19: 3.689, 20: 3.735, 21: 3.778, 22: 3.819, 23: 3.858, 24: 3.895, 25: 3.931, 26: 3.964, 27: 3.997, 28: 4.027, 29: 4.057, 30: 4.086, 31: 4.113, 32: 4.139, 33: 4.165, 34: 4.189, 35: 4.213, 36: 4.236, 37: 4.259, 38: 4.28, 39: 4.301, 40: 4.322, 41: 4.341, 42: 4.361, 43: 4.379, 44: 4.398, 45: 4.415, 46: 4.433, 47: 4.45, 48: 4.466, 49: 4.482, 50: 4.498}
    if N in d2_values:
        return d2_values.get(N)
    else:
        return 3.4873 + 0.0250141 * N - 0.00009823 * N**2

def d3(N):
    # d3(N) is the standard deviation of the range of N observations from a normal population with σ = 1.
    # Thus, if r is the range of a sample of N observations from a normal distribution with standard deviation = σ, then stdev(r) = d3(N)σ.
    d3_values = {2: 0.8525,  3: 0.8884,  4: 0.8798,  5: 0.8641,  6: 0.848,  7: 0.8332,  8: 0.8198,  9: 0.8078,  10: 0.7971,  11: 0.7873,  12: 0.7785,  13: 0.7704,  14: 0.763,  15: 0.7562,  16: 0.7499,  17: 0.7441,  18: 0.7386,  19: 0.7335,  20: 0.7287,  21: 0.7242,  22: 0.7199,  23: 0.7159,  24: 0.7121,  25: 0.7084}
    if N in d3_values:
        return d3_values.get(N)
    else:
        return 0.80818 - 0.0051871 * N - 0.00005098 * N**2 - 0.00000019 * N**3

def d4(N):
    d4_values = {2: 0.954,  3: 1.588,  4: 1.978,  5: 2.257,  6: 2.472,  7: 2.645,  8: 2.791,  9: 2.915,  10: 3.024,  11: 3.121,  12: 3.207,  13: 3.285,  14: 3.356,  15: 3.422,  16: 3.482,  17: 3.538,  18: 3.591,  19: 3.64,  20: 3.686,  21: 3.73,  22: 3.771,  23: 3.811,  24: 3.847,  25: 3.883}
    if N in d4_values:
        return d4_values.get(N)
    else:
        return 2.88606 + 0.051313 * N - 0.00049243 * N**2 + 0.00000188 * N**3


def c5(N):
    # unbiasing constant c5
    return (1-c4(N)**2)**0.5

def c4_(n):
    # unbiasing constant c4'
    # used in formulas for the square root of MSSD method of estimating sigma
    constants = {
        2: 0.79785, 3: 0.87153, 4: 0.905763, 5: 0.925222, 6: 0.937892, 7: 0.946837, 8: 0.953503, 9: 0.958669, 10: 0.962793, 11: 0.966163, 12: 0.968968, 13: 0.971341, 14: 0.973375, 15: 0.975137, 16: 0.976679, 17: 0.978039,
        18: 0.979249, 19: 0.980331, 20: 0.981305, 21: 0.982187, 22: 0.982988, 23: 0.98372, 24: 0.984391, 25: 0.985009, 26: 0.985579, 27: 0.986107, 28: 0.986597, 29: 0.987054, 30: 0.98748, 31: 0.987878, 32: 0.988252, 33: 0.988603,
        34: 0.988934, 35: 0.989246, 36: 0.98954, 37: 0.989819, 38: 0.990083, 39: 0.990333, 40: 0.990571, 41: 0.990797, 42: 0.991013, 43: 0.991218, 44: 0.991415, 45: 0.991602, 46: 0.991782, 47: 0.991953, 48: 0.992118, 49: 0.992276,
        50: 0.992427, 51: 0.992573, 52: 0.992713, 53: 0.992848, 54: 0.992978, 55: 0.993103, 56: 0.993224, 57: 0.99334, 58: 0.993452, 59: 0.993561, 60: 0.993666, 61: 0.993767, 62: 0.993866, 63: 0.993961, 64: 0.994053, 65: 0.994142,
        66: 0.994229, 67: 0.994313, 68: 0.994395, 69: 0.994474, 70: 0.994551, 71: 0.994626, 72: 0.994699, 73: 0.994769, 74: 0.994838, 75: 0.994905, 76: 0.99497, 77: 0.995034, 78: 0.995096, 79: 0.995156, 80: 0.995215, 81: 0.995272,
        82: 0.995328, 83: 0.995383, 84: 0.995436, 85: 0.995489, 86: 0.995539, 87: 0.995589, 88: 0.995638, 89: 0.995685, 90: 0.995732, 91: 0.995777, 92: 0.995822, 93: 0.995865, 94: 0.995908, 95: 0.995949, 96: 0.99599, 97: 0.99603,
        98: 0.996069, 99: 0.996108, 100: 0.996145, 101: 0.996182, 102: 0.996218, 103: 0.996253, 104: 0.996288, 105: 0.996322, 106: 0.996356, 107: 0.996389, 108: 0.996421, 109: 0.996452, 110: 0.996483, 111: 0.996514, 112: 0.996544, 113: 0.996573,
        114: 0.996602, 115: 0.996631, 116: 0.996658, 117: 0.996686, 118: 0.996713, 119: 0.996739, 120: 0.996765, 121: 0.996791, 122: 0.996816, 123: 0.996841, 124: 0.996865, 125: 0.996889, 126: 0.996913, 127: 0.996936, 128: 0.996959, 129: 0.996982,
        130: 0.997004, 131: 0.997026, 132: 0.997047, 133: 0.997069, 134: 0.997089, 135: 0.99711, 136: 0.99713, 137: 0.99715, 138: 0.99717, 139: 0.997189, 140: 0.997209, 141: 0.997227, 142: 0.997246, 143: 0.997264, 144: 0.997282, 145: 0.9973,
        146: 0.997318, 147: 0.997335, 148: 0.997352, 149: 0.997369, 150: 0.997386, 151: 0.997402, 152: 0.997419, 153: 0.997435, 154: 0.99745, 155: 0.997466, 156: 0.997481, 157: 0.997497, 158: 0.997512, 159: 0.997526, 160: 0.997541, 161: 0.997555,
        162: 0.99757, 163: 0.997584, 164: 0.997598, 165: 0.997612, 166: 0.997625, 167: 0.997639, 168: 0.997652, 169: 0.997665, 170: 0.997678, 171: 0.997691, 172: 0.997703, 173: 0.997716, 174: 0.997728, 175: 0.997741, 176: 0.997753, 177: 0.997765,
        178: 0.997776, 179: 0.997788, 180: 0.9978, 181: 0.997811, 182: 0.997822, 183: 0.997834, 184: 0.997845, 185: 0.997856, 186: 0.997866, 187: 0.997877, 188: 0.997888, 189: 0.997898, 190: 0.997909, 191: 0.997919, 192: 0.997929, 193: 0.997939,
        194: 0.997949, 195: 0.997959, 196: 0.997969, 197: 0.997978, 198: 0.997988, 199: 0.997997, 200: 0.998007, 201: 0.998016, 202: 0.998025, 203: 0.998034, 204: 0.998043, 205: 0.998052, 206: 0.998061, 207: 0.99807, 208: 0.998078, 209: 0.998087,
        210: 0.998095, 211: 0.998104, 212: 0.998112, 213: 0.99812, 214: 0.998128, 215: 0.998137, 216: 0.998145, 217: 0.998152, 218: 0.99816, 219: 0.998168, 220: 0.998176, 221: 0.998184, 222: 0.998191, 223: 0.998199, 224: 0.998206, 225: 0.998214,
        226: 0.998221, 227: 0.998228, 228: 0.998235, 229: 0.998242, 230: 0.99825, 231: 0.998257, 232: 0.998263, 233: 0.99827, 234: 0.998277, 235: 0.998284, 236: 0.998291, 237: 0.998297, 238: 0.998304, 239: 0.998311, 240: 0.998317, 241: 0.998323,
        242: 0.99833, 243: 0.998336, 244: 0.998342, 245: 0.998349, 246: 0.998355, 247: 0.998361, 248: 0.998367, 249: 0.998373, 250: 0.998379, 251: 0.998385, 252: 0.998391, 253: 0.998397, 254: 0.998403, 255: 0.998408, 256: 0.998414, 257: 0.99842,
        258: 0.998425, 259: 0.998431, 260: 0.998436, 261: 0.998442, 262: 0.998447, 263: 0.998453, 264: 0.998458, 265: 0.998463, 266: 0.998469, 267: 0.998474, 268: 0.998479, 269: 0.998484, 270: 0.998489, 271: 0.998495, 272: 0.9985, 273: 0.998505,
        274: 0.99851, 275: 0.998515, 276: 0.998519, 277: 0.998524, 278: 0.998529, 279: 0.998534, 280: 0.998539, 281: 0.998544, 282: 0.998548, 283: 0.998553, 284: 0.998558, 285: 0.998562, 286: 0.998567, 287: 0.998571, 288: 0.998576, 289: 0.99858,
        290: 0.998585, 291: 0.998589, 292: 0.998593, 293: 0.998598, 294: 0.998602, 295: 0.998606, 296: 0.998611, 297: 0.998615, 298: 0.998619, 299: 0.998623, 300: 0.998627, 301: 0.998632, 302: 0.998636, 303: 0.99864, 304: 0.998644, 305: 0.998648,
        306: 0.998652, 307: 0.998656, 308: 0.99866, 309: 0.998664, 310: 0.998668, 311: 0.998671, 312: 0.998675, 313: 0.998679, 314: 0.998683, 315: 0.998687, 316: 0.99869, 317: 0.998694, 318: 0.998698, 319: 0.998701, 320: 0.998705, 321: 0.998709,
        322: 0.998712, 323: 0.998716, 324: 0.99872, 325: 0.998723, 326: 0.998727, 327: 0.99873, 328: 0.998734, 329: 0.998737, 330: 0.99874, 331: 0.998744, 332: 0.998747, 333: 0.998751, 334: 0.998754, 335: 0.998757, 336: 0.998761, 337: 0.998764,
        338: 0.998767, 339: 0.99877, 340: 0.998774, 341: 0.998777, 342: 0.99878, 343: 0.998783, 344: 0.998786, 345: 0.99879, 346: 0.998793, 347: 0.998796, 348: 0.998799, 349: 0.998802, 350: 0.998805, 351: 0.998808, 352: 0.998811, 353: 0.998814,
        354: 0.998817, 355: 0.99882, 356: 0.998823, 357: 0.998826, 358: 0.998829, 359: 0.998832, 360: 0.998835, 361: 0.998837, 362: 0.99884, 363: 0.998843, 364: 0.998846, 365: 0.998849, 366: 0.998851, 367: 0.998854, 368: 0.998857, 369: 0.99886,
        370: 0.998862, 371: 0.998865, 372: 0.998868, 373: 0.998871, 374: 0.998873, 375: 0.998876, 376: 0.998879, 377: 0.998881, 378: 0.998884, 379: 0.998886, 380: 0.998889, 381: 0.998892, 382: 0.998894, 383: 0.998897, 384: 0.998899, 385: 0.998902,
        386: 0.998904, 387: 0.998907, 388: 0.998909, 389: 0.998912, 390: 0.998914, 391: 0.998917, 392: 0.998919, 393: 0.998921, 394: 0.998924, 395: 0.998926, 396: 0.998929, 397: 0.998931, 398: 0.998933, 399: 0.998936, 400: 0.998938, 401: 0.99894,
        402: 0.998943, 403: 0.998945, 404: 0.998947, 405: 0.99895, 406: 0.998952, 407: 0.998954, 408: 0.998956, 409: 0.998959, 410: 0.998961, 411: 0.998963, 412: 0.998965, 413: 0.998967, 414: 0.99897, 415: 0.998972, 416: 0.998974, 417: 0.998976,
        418: 0.998978, 419: 0.99898, 420: 0.998982, 421: 0.998985, 422: 0.998987, 423: 0.998989, 424: 0.998991, 425: 0.998993, 426: 0.998995, 427: 0.998997, 428: 0.998999, 429: 0.999001, 430: 0.999003, 431: 0.999005, 432: 0.999007, 433: 0.999009,
        434: 0.999011, 435: 0.999013, 436: 0.999015, 437: 0.999017, 438: 0.999019, 439: 0.999021, 440: 0.999023, 441: 0.999025, 442: 0.999027, 443: 0.999028, 444: 0.99903, 445: 0.999032, 446: 0.999034, 447: 0.999036, 448: 0.999038, 449: 0.99904,
        450: 0.999042, 451: 0.999043, 452: 0.999045, 453: 0.999047, 454: 0.999049, 455: 0.999051, 456: 0.999052, 457: 0.999054, 458: 0.999056, 459: 0.999058, 460: 0.99906, 461: 0.999061, 462: 0.999063, 463: 0.999065, 464: 0.999067, 465: 0.999068,
        466: 0.99907, 467: 0.999072, 468: 0.999073, 469: 0.999075, 470: 0.999077, 471: 0.999078, 472: 0.99908, 473: 0.999082, 474: 0.999084, 475: 0.999085, 476: 0.999087, 477: 0.999088, 478: 0.99909, 479: 0.999092, 480: 0.999093, 481: 0.999095,
        482: 0.999097, 483: 0.999098, 484: 0.9991, 485: 0.999101, 486: 0.999103, 487: 0.999104, 488: 0.999106, 489: 0.999108, 490: 0.999109, 491: 0.999111, 492: 0.999112, 493: 0.999114, 494: 0.999115, 495: 0.999117, 496: 0.999118, 497: 0.99912,
        498: 0.999121, 499: 0.999123, 500: 0.999124
    }
    return constants.get(n)

def gamma(N, one_alpha):
    # used in calculating the confidence interval for Z
    
    gamma_dict = {
        0.8: {5: 3.544, 6: 3.485, 7: 3.443, 8: 3.413, 9: 3.39, 10: 3.372, 12: 3.345, 14: 3.326, 16: 3.312, 18: 3.301, 20: 3.293, 25: 3.278, 30: 3.268, 35: 3.261, 40: 3.255, 50: 3.248, 60: 3.243, 80: 3.237, 100: 3.233, 101: 3.219}, 
        0.85: {5: 4.138, 6: 4.078, 7: 4.035, 8: 4.003, 9: 3.979, 10: 3.96, 12: 3.931, 14: 3.911, 16: 3.986, 18: 3.884, 20: 3.875, 25: 3.858, 30: 3.848, 35: 3.84, 40: 3.834, 50: 3.826, 60: 3.821, 80: 3.814, 100: 3.81, 101: 3.794}, 
        0.9: {5: 4.961, 6: 4.903, 7: 4.861, 8: 4.829, 9: 4.804, 10: 4.783, 12: 4.753, 14: 4.732, 16: 4.716, 18: 4.703, 20: 4.693, 25: 4.675, 30: 4.664, 35: 4.655, 40: 4.649, 50: 4.64, 60: 4.634, 80: 4.627, 100: 4.623, 101: 4.605}, 
        0.95: {5: 6.35, 6: 6.3, 7: 6.26, 8: 6.229, 9: 6.204, 10: 6.183, 12: 6.152, 14: 6.13, 16: 6.113, 18: 6.099, 20: 6.089, 25: 6.069, 30: 6.056, 35: 6.047, 40: 6.04, 50: 6.031, 60: 6.024, 80: 6.016, 100: 6.011, 101: 5.991}, 
        0.99: {5: 9.75, 6: 9.636, 7: 9.567, 8: 9.52, 9: 9.484, 10: 9.457, 12: 9.416, 14: 9.387, 16: 9.365, 18: 9.348, 20: 9.335, 25: 9.31, 30: 9.294, 35: 9.282, 40: 9.274, 50: 9.262, 60: 9.253, 80: 9.244, 100: 9.238, 101: 9.21}
    }
    
    gamma_table = pd.DataFrame(gamma_dict)
    
    # handle N > 100
    N = (101 if N > 100 else N)       
    
    if one_alpha in gt.columns:
        return np.interp(N, gamma_table.index, gamma_table[one_alpha])
        
    elif N in gt.index:
        return np.interp(one_alpha, gamma_table.T.index, gamma_table.T[N])
    else:
        lower_val = [val for val in gamma_table.index if val < N][-1]
        upper_val = [val for val in gamma_table.index if val > N][0]
        
        y_upper = np.interp(one_alpha, gamma_table.T.index, gamma_table.T[upper_val])
        y_lower = np.interp(one_alpha, gamma_table.T.index, gamma_table.T[lower_val])
        
        return (abs(y_upper-y_lower)/abs(upper_val-lower_val))*abs(N-lower_val) + y_upper