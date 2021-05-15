import numpy as np
import unittest
from mock import Mock
from parameterized import parameterized

from ..core.fit_modules.fit_mieze import Fit_MIEZE


class Test_ContrastProcessing(unittest.TestCase):

    def setUp(self) -> None:

        # Set up the used class
        self.contrast_proc = Fit_MIEZE()

        def get_axis(axis_name):
            if axis_name == self.contrast_proc.para_dict['foil_name']:
                return [i for i in range(8)]

        def get_axis_len(axis_name):
            if axis_name == self.contrast_proc.para_dict['tcha_name']:
                return 16
            if axis_name == self.contrast_proc.para_dict['foil_name']:
                return 8

        self.target = Mock(
            get_axis_len=Mock(wraps=get_axis_len),
            get_axis=Mock(wraps=get_axis))

        # Set up the used mask
        self.masks = {}
        self.masks['flat'] = np.ones((128, 128), dtype=np.uint32)
        self.masks['quarter'] = np.zeros((128, 128), dtype=np.uint32)
        self.masks['quarter'][0:64, 0:64] = 1

        # set up the used data
        self.data = {}
        self.data['sinus'] = np.zeros((1, 1, 5, 8, 16), dtype=np.uint32)
        for echo in range(5):
            for time_channel in range(16):
                value = 10000 / (echo + 1) * np.sin(np.pi * time_channel / 15) + 10000
                for foil in range(8):
                    self.data['sinus'][0, 0, echo, foil, time_channel] = value + 1000 * foil

        self.data['flat'] = np.ones((1, 1, 5, 8, 16), dtype=np.uint32)

    result_0 = [
        4.42368000e+08, 5.10492672e+08, 5.75635456e+08, 6.34945536e+08,
        6.85867008e+08, 7.26138880e+08, 7.53991680e+08, 7.68245760e+08,
        7.68245760e+08, 7.53991680e+08, 7.26138880e+08, 6.85867008e+08,
        6.34945536e+08, 5.75635456e+08, 5.10492672e+08, 4.42368000e+08]
    result_1 = [
        1769472000.0, 2041970688.0, 2302541824.0, 2539782144.0,
        2743468032.0, 2904555520.0, 3015966720.0, 3072983040.0,
        3072983040.0, 3015966720.0, 2904555520.0, 2743468032.0,
        2539782144.0, 2302541824.0, 2041970688.0, 1769472000.0]
    result_2 = [32768.0 for i in range(16)]
    result_3 = [131072.0 for i in range(16)]

    result_0_foil_in = [
        45056000.0, 53571584.0, 61714432.0, 69128192.0,
        75493376.0, 80527360.0, 84008960.0, 85790720.0,
        85790720.0, 84008960.0, 80527360.0, 75493376.0,
        69128192.0, 61714432.0, 53571584.0, 45056000.0]
    result_1_foil_in = [
        180224000.0, 214286336.0, 246857728.0, 276512768.0,
        301973504.0, 322109440.0, 336035840.0, 343162880.0,
        343162880.0, 336035840.0, 322109440.0, 301973504.0,
        276512768.0, 246857728.0, 214286336.0, 180224000.0]
    result_2_foil_in = [4096.0 for i in range(16)]
    result_3_foil_in = [16384.0 for i in range(16)]

    @parameterized.expand([
        # Assume we have not foil in
        ('test_sinus_quarter', 'sinus', 'quarter', None, result_0),
        ('test_sinus_flat', 'sinus', 'flat', None, result_1),
        ('test_flat_quarter', 'flat', 'quarter', None, result_2),
        ('test_flat_flat', 'flat', 'flat', None, result_3),

        # Assume we have foil in
        ('test_sinus_quarter_foil_in', 'sinus', 'quarter', 1, result_0_foil_in),
        ('test_sinus_flat_foil_in', 'sinus', 'flat', 1, result_1_foil_in),
        ('test_flat_quarter_foil_in', 'flat', 'quarter', 1, result_2_foil_in),
        ('test_flat_flat_foil_in', 'flat', 'flat', 1, result_3_foil_in),
    ])
    def test_combineData_sum(self, _, data_id, mask_id, foil_in, expectation):
        result = self.contrast_proc.combineData(
            self.data[data_id][0, 0, 0], self.target, self.masks[mask_id], [1 for i in range(8)], foil_in)
        self.assertEqual(len(expectation), len(result.tolist()))
        self.assertEqual(expectation, result.tolist())

    result_0_no_sum = [(np.array([
        40960000, 49475584, 57618432, 65032192,
        71397376, 76431360, 79912960, 81694720,
        81694720, 79912960, 76431360, 71397376,
        65032192, 57618432, 49475584, 40960000]) + 4096000 * j).tolist()
                       for j in range(8)]
    result_1_no_sum = [(np.array([
        163840000, 197902336, 230473728, 260128768,
        285589504, 305725440, 319651840, 326778880,
        326778880, 319651840, 305725440, 285589504,
        260128768, 230473728, 197902336, 163840000]) + 16384000 * j).tolist()
                       for j in range(8)]
    result_2_no_sum = [[4096 for i in range(16)] for j in range(8)]
    result_3_no_sum = [[16384 for i in range(16)] for j in range(8)]

    result_2_no_sum_foil_in = [[4096 if j == 1 else 0 for i in range(16)] for j in range(8)]
    result_3_no_sum_foil_in = [[16384 if j == 1 else 0 for i in range(16)] for j in range(8)]

    @parameterized.expand([
        # Assume we have not foil in
        ('test_sinus_quarter', 'sinus', 'quarter', None, result_0_no_sum),
        ('test_sinus_flat', 'sinus', 'flat', None, result_1_no_sum),
        ('test_flat_quarter', 'flat', 'quarter', None, result_2_no_sum),
        ('test_flat_flat', 'flat', 'flat', None, result_3_no_sum),

        # Assume we have foil in
        # ('test_sinus_quarter_foil_in', 'sinus', 'quarter', 1, result_0_foil_in),
        # ('test_sinus_flat_foil_in', 'sinus', 'flat', 1,result_1_foil_in),
        ('test_flat_quarter_foil_in', 'flat', 'quarter', 1, result_2_no_sum_foil_in),
        ('test_flat_flat_foil_in', 'flat', 'flat', 1, result_3_no_sum_foil_in),
    ])
    def test_combineData_no_sum(self, _, data_id, mask_id, foil_in, expectation):
        result = self.contrast_proc.combineData(
            self.data[data_id][0, 0, 0], self.target, self.masks[mask_id], [1 for i in range(8)], foil_in, False)
        self.assertEqual((8, 16), result.shape)
        self.assertEqual(expectation, result.tolist())

    sin_fit_result_0 = [158660831.20292726, 8732.35587763226, 636261717.076139, 6308.30202821826]
    sin_fit_result_1 = [634643311.0327941, 17467.52873872937, 2545046869.289102, 12612.114380148403]
    sin_fit_result_3 = [0, 0, 0, 0]

    @parameterized.expand([
        # Test the behaviour
        ('test_sinus_quarter_mask', result_0, sin_fit_result_0),
        ('test_sinus_flat_mask', result_1, sin_fit_result_1),

        # Test flat data failures
        ('test_sinus_flat_0', result_2, sin_fit_result_3),
        ('test_sinus_flat_1', result_3, sin_fit_result_3),
    ])
    def test_fitContrastSinus_summed_foils(self, _, data, expectation):
        result = self.contrast_proc.fitContrastSinus(np.array(data), self.target, 1)
        self.assertEqual([round(e, 4) for e in expectation], [round(e, 4) for e in result])

    sin_fit_result_no_sum_0 = [
        [19989315.244484395, 2773.698604504637, 65164290.501007386, 2018.1100507918757],
        [19936488.97088189, 2867.3996156014286, 69271271.29034916, 2080.7341146361773],
        [19890766.44693641, 2957.7689759631066, 73376733.9382977, 2141.5055178450534],
        [19850780.447497267, 3045.169749951395, 77480977.43763815, 2200.5819899567036],
        [19815498.207075443, 3129.8998183752415, 81584226.23807412, 2258.099677523916],
        [19784123.952537753, 3212.207712806339, 85686652.31140505, 2314.1771298268654],
        [19756033.928402692, 3292.3036921439034, 89788389.76548739, 2368.918398293282],
        [19730728.177680984, 3370.3677714443284, 93889544.69569962, 2422.4154366084504]]
    sin_fit_result_no_sum_1 = [
        [79957260.97794648, 5547.3972207454, 260657162.00403598, 4036.220104908728],
        [79745955.88353507, 5734.799247952378, 277085085.1613992, 4161.468241130187],
        [79563055.03018595, 5915.537948780161, 293506936.6966338, 4283.011036488646],
        [79403111.67714441, 6090.339490373287, 309923910.7206162, 4401.16399023169],
        [79261983.22443525, 6259.799665830539, 326336905.91441804, 4516.199347034302],
        [79136486.63200784, 6424.415390611166, 342746610.1800615, 4628.354261506158],
        [79024126.90719098, 6584.607363261871, 359153559.95815766, 4737.836787944616],
        [78922918.96423979, 6740.735530905086, 375558180.0580458, 4844.830879820695]]
    sin_fit_result_no_sum_3 = [[0, 0, 0, 0] for j in range(8)]

    @parameterized.expand([
        # Test the behaviour
        ('test_sinus_quarter_mask', result_0_no_sum, sin_fit_result_no_sum_0),
        ('test_sinus_flat_mask', result_1_no_sum, sin_fit_result_no_sum_1),

        # Test flat data failures
        ('test_sinus_flat_0', result_2_no_sum, sin_fit_result_no_sum_3),
        ('test_sinus_flat_1', result_3_no_sum, sin_fit_result_no_sum_3),
    ])
    def test_fitContrastSinus_not_summed_foils(self, _, data, expectation):
        result = self.contrast_proc.fitContrastSinus(np.array(data), self.target, 1)
        self.assertEqual(
            [[round(e, 4) for e in expectation_foil]
             for expectation_foil in expectation],
            [[round(e, 4) for e in result_foil]
             for result_foil in result])
