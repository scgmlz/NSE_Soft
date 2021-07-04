import numpy as np
import unittest
from miezepy.core.module_result import ResultStructure
from mock import Mock
from parameterized import parameterized

from ..core.fit_modules.fit_mieze import Fit_MIEZE


class Test_ContrastProcessing_fit(unittest.TestCase):
    def setUp(self) -> None:

        # Set up the used class
        self.contrast_proc = Fit_MIEZE()
        self.contrast_proc.para_dict['foils_in_echo'] = [[1 for i in range(8)]]
        self.contrast_proc.para_dict['processors'] = 6

        # Set up the fake return function for the axes
        def get_axis(axis_name):
            if axis_name == self.contrast_proc.para_dict['foil_name']:
                return [i for i in range(8)]
            if axis_name == self.contrast_proc.para_dict['meas_name']:
                return [0]
            if axis_name == self.contrast_proc.para_dict['para_name']:
                return [0]
            if axis_name == self.contrast_proc.para_dict['tcha_name']:
                return [i for i in range(16)]
            if axis_name == self.contrast_proc.para_dict['echo_name']:
                return [0]

        # Set up the fake return function for the axis length
        def get_axis_len(axis_name):
            if axis_name == self.contrast_proc.para_dict['tcha_name']:
                return 16
            if axis_name == self.contrast_proc.para_dict['foil_name']:
                return 8
            if axis_name == self.contrast_proc.para_dict['meas_name']:
                return 1
            if axis_name == self.contrast_proc.para_dict['para_name']:
                return 1
            if axis_name == self.contrast_proc.para_dict['echo_name']:
                return 1

        # Now nock it in
        self.target = Mock(
            get_axis_len=Mock(wraps=get_axis_len),
            get_axis=Mock(wraps=get_axis),
            map=np.zeros((1, 1, 1, 1, 1), dtype=int),
            metadata_objects=[{'Monitor': 10}],
            metadata_addresses=[0],
            data_objects=[Mock(meta_address=[0])])

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


class Test_ContrastProcessing_dispatching(unittest.TestCase):
    def setUp(self) -> None:

        # Set up the used class
        self.contrast_proc = Fit_MIEZE()
        self.contrast_proc.para_dict['foils_in_echo'] = [[1 for i in range(8)] for j in range(30)]
        self.contrast_proc.para_dict['processors'] = 1

        # Set up the fake return function for the axes
        def get_axis(axis_name):
            if axis_name == self.contrast_proc.para_dict['foil_name']:
                return [i for i in range(8)]
            if axis_name == self.contrast_proc.para_dict['meas_name']:
                return [0]
            if axis_name == self.contrast_proc.para_dict['para_name']:
                return [i for i in range(2)]
            if axis_name == self.contrast_proc.para_dict['tcha_name']:
                return [i for i in range(16)]
            if axis_name == self.contrast_proc.para_dict['echo_name']:
                return [i for i in range(3)]

        # Set up the fake return function for the axis length
        def get_axis_len(axis_name):
            if axis_name == self.contrast_proc.para_dict['tcha_name']:
                return 16
            if axis_name == self.contrast_proc.para_dict['foil_name']:
                return 8
            if axis_name == self.contrast_proc.para_dict['meas_name']:
                return 1
            if axis_name == self.contrast_proc.para_dict['para_name']:
                return 2
            if axis_name == self.contrast_proc.para_dict['echo_name']:
                return 3

        # Now nock it in
        self.target = Mock(
            get_axis_len=Mock(wraps=get_axis_len),
            get_axis=Mock(wraps=get_axis),
            map=np.zeros((2, 1, 3, 1, 1), dtype=int),
            metadata_objects=[{'Monitor': 10}],
            metadata_addresses=[0],
            data_objects=[Mock(meta_address=[0])])

        # Set up the used mask
        self.masks = {}
        self.masks['flat'] = np.ones((128, 128), dtype=np.uint32)

        # set up the used data
        self.data = {}
        self.data['sinus'] = np.zeros((2, 1, 3, 8, 16), dtype=np.uint32)
        for echo in range(3):
            for time_channel in range(16):
                value = 10000 / (echo + 1) * np.sin(np.pi * time_channel / 15) + 10000
                for foil in range(8):
                    self.data['sinus'][:, 0, echo, foil, time_channel] = value + 1000 * foil

    expectation_summed = {
        0: {0: {
            0: [63464331.10327941, 1746.7528738729368, 254504686.9289102, 1261.2114380148403],
            1: [31311876.368920464, 1626.348071201755, 215807301.55453768, 1161.3766111314662],
            2: [20766315.192216076, 1580.7158784408177, 202875963.84547612, 1126.011724205858]}},
        1: {0: {
            0: [63464331.10327941, 1746.7528738729368, 254504686.9289102, 1261.2114380148403],
            1: [31311876.368920464, 1626.348071201755, 215807301.55453768, 1161.3766111314662],
            2: [20766315.192216076, 1580.7158784408177, 202875963.84547612, 1126.011724205858]}}}
    expectation_not_summed = {
        0: {0: {
            0: [
                [7995726.097794647, 554.7397220745399, 26065716.200403597, 403.6220104908728],
                [7974595.588353507, 573.4799247952378, 27708508.516139917, 416.14682411301874],
                [7956305.503018595, 591.5537948780161, 29350693.66966338, 428.30110364886457],
                [7940311.167714441, 609.0339490373287, 30992391.07206162, 440.11639902316904],
                [7926198.322443525, 625.979966583054, 32633690.591441803, 451.6199347034302],
                [7913648.663200784, 642.4415390611166, 34274661.01800615, 462.8354261506158],
                [7902412.690719098, 658.4607363261871, 35915355.99581577, 473.7836787944616],
                [7892291.896423979, 674.0735530905087, 37555818.00580458, 484.48308798206955]],
            1: [
                [3933623.170242307, 508.2398181564821, 21237560.78288595, 364.3278123100041],
                [3926906.379723572, 528.2095019007429, 22877316.690226793, 378.1312320688392],
                [3921171.8841295997, 547.4227225973093, 24516870.792402256, 391.44660310955487],
                [3916217.4778548838, 565.7444648737287, 26156265.07559168, 404.31566921662403],
                [3911893.383997222, 583.8958400370987, 27795531.25770119, 416.7997960249483],
                [3908085.8794981698, 601.2811313248606, 29434692.22740513, 428.91354188414624],
                [3904707.1870936654, 618.1665039066654, 31073766.279702365, 440.693815632316],
                [3901688.4364666967, 634.5935787403707, 32712767.554104548, 452.16677992386894]],
            2: [
                [2605333.7927724877, 491.114668569889, 19623196.395748757, 350.2130288174184],
                [2602049.5366792255, 511.48324135839005, 21262256.169329103, 364.5395372304702],
                [2599260.0090530687, 531.2125831768174, 22901206.56673359, 378.32861519239907],
                [2596864.9228702853, 550.2233831223945, 24540082.188914046, 391.63185618627557],
                [2594784.76696657, 568.589898877593, 26178894.565180194, 404.4973292782441],
                [2592960.6214828244, 586.3742724523368, 27817655.368610382, 416.96564295789705],
                [2591348.795446686, 603.6291879965434, 29456374.028673045, 429.07148458348547],
                [2589913.7559411493, 621.1995192255418, 31095057.41440062, 442.1482951004685]]}},
        1: {0: {
            0: [
                [7995726.097794647, 554.7397220745399, 26065716.200403597, 403.6220104908728],
                [7974595.588353507, 573.4799247952378, 27708508.516139917, 416.14682411301874],
                [7956305.503018595, 591.5537948780161, 29350693.66966338, 428.30110364886457],
                [7940311.167714441, 609.0339490373287, 30992391.07206162, 440.11639902316904],
                [7926198.322443525, 625.979966583054, 32633690.591441803, 451.6199347034302],
                [7913648.663200784, 642.4415390611166, 34274661.01800615, 462.8354261506158],
                [7902412.690719098, 658.4607363261871, 35915355.99581577, 473.7836787944616],
                [7892291.896423979, 674.0735530905087, 37555818.00580458, 484.48308798206955]],
            1: [
                [3933623.170242307, 508.2398181564821, 21237560.78288595, 364.3278123100041],
                [3926906.379723572, 528.2095019007429, 22877316.690226793, 378.1312320688392],
                [3921171.8841295997, 547.4227225973093, 24516870.792402256, 391.44660310955487],
                [3916217.4778548838, 565.7444648737287, 26156265.07559168, 404.31566921662403],
                [3911893.383997222, 583.8958400370987, 27795531.25770119, 416.7997960249483],
                [3908085.8794981698, 601.2811313248606, 29434692.22740513, 428.91354188414624],
                [3904707.1870936654, 618.1665039066654, 31073766.279702365, 440.693815632316],
                [3901688.4364666967, 634.5935787403707, 32712767.554104548, 452.16677992386894]],
            2: [
                [2605333.7927724877, 491.114668569889, 19623196.395748757, 350.2130288174184],
                [2602049.5366792255, 511.48324135839005, 21262256.169329103, 364.5395372304702],
                [2599260.0090530687, 531.2125831768174, 22901206.56673359, 378.32861519239907],
                [2596864.9228702853, 550.2233831223945, 24540082.188914046, 391.63185618627557],
                [2594784.76696657, 568.589898877593, 26178894.565180194, 404.4973292782441],
                [2592960.6214828244, 586.3742724523368, 27817655.368610382, 416.96564295789705],
                [2591348.795446686, 603.6291879965434, 29456374.028673045, 429.07148458348547],
                [2589913.7559411493, 621.1995192255418, 31095057.41440062, 442.1482951004685]]}}}

    @parameterized.expand([
        # Test the behaviour
        ('tested_summed_dispatcher', True, expectation_summed),
        # Test the behaviour
        ('tested_not_summed_dispatcher', False, expectation_not_summed)
    ])
    def test_calcContrastFit(self, _, sum_foils, expectation):
        result = self.contrast_proc.calcContrastFit(
            [i for i in range(2)], self.data['sinus'],
            self.target, Mock(mask=self.masks['flat']),
            foil=None, sum_foils=sum_foils)
        self.maxDiff = None
        self.assertEqual(expectation, result)


class Test_calcContrastMain(unittest.TestCase):
    def setUp(self) -> None:

        # Set up the used class
        self.contrast_proc = Fit_MIEZE()
        self.contrast_proc.para_dict['foils_in_echo'] = [[1 for i in range(8)] for j in range(30)]
        self.contrast_proc.para_dict['processors'] = 1

        # Set up the fake return function for the axes
        def get_axis(axis_name):
            if axis_name == self.contrast_proc.para_dict['foil_name']:
                return [i for i in range(8)]
            if axis_name == self.contrast_proc.para_dict['meas_name']:
                return [0]
            if axis_name == self.contrast_proc.para_dict['para_name']:
                return [str(i) for i in range(2)]
            if axis_name == self.contrast_proc.para_dict['tcha_name']:
                return [i for i in range(16)]
            if axis_name == self.contrast_proc.para_dict['echo_name']:
                return [i for i in range(3)]

        # Set up the fake return function for the axis length
        def get_axis_len(axis_name):
            if axis_name == self.contrast_proc.para_dict['tcha_name']:
                return 16
            if axis_name == self.contrast_proc.para_dict['foil_name']:
                return 8
            if axis_name == self.contrast_proc.para_dict['meas_name']:
                return 1
            if axis_name == self.contrast_proc.para_dict['para_name']:
                return 2
            if axis_name == self.contrast_proc.para_dict['echo_name']:
                return 3

        names = ['Parameter', 'Measurement', 'Echo Time', 'Foil', 'Time Channel']

        # Now nock it in
        self.target = Mock(
            get_axis_len=Mock(wraps=get_axis_len),
            get_axis=Mock(wraps=get_axis),
            map=np.zeros((2, 1, 3, 1, 1), dtype=int),
            metadata_objects=[{'Monitor': 10}],
            metadata_addresses=[0],
            data_objects=[Mock(meta_address=[0])],
            axes=Mock(names=names))

        # Set up the used mask
        self.masks = {}
        self.masks['flat'] = np.ones((128, 128), dtype=np.uint32)

        # set up the used data
        self.data = {}
        self.data['sinus'] = np.zeros((2, 1, 3, 8, 16), dtype=np.uint32)
        for echo in range(3):
            for time_channel in range(16):
                value = 10000 / (echo + 1) * np.sin(np.pi * time_channel / 15) + 10000
                for foil in range(8):
                    self.data['sinus'][:, 0, echo, foil, time_channel] = value + 1000 * foil
        self.data['sinus'] *= 2

        self.results = ResultStructure(mode='Dict')

        local_results = self.results.generateResult(name='Contrast mode')
        local_results['Mode'] = 'Corrected'
        local_results.setComplete()

        local_results = self.results.generateResult(name='Corrected Phase')
        local_results['Shift'] = self.data['sinus']
        local_results.setComplete()

    expectation_summed = {'Axis': {'0': [0, 1, 2], '1': [0, 1, 2]},
                          'Contrast': {'0': [0.37209263219565897, 1.1615838600179353, 1.777224782509143],
                                       '1': [0.37209263219565897, 1.1615838600179353, 1.777224782509143]},
                          'Contrast_error': {
                              '0': [1.3135277632258316e-05, 8.432927545257018e-05, 2.589879232666367e-05],
                              '1': [1.3135277632258316e-05, 8.432927545257018e-05, 2.589879232666367e-05]},
                          'Background': None, 'Foil': None}

    expectation_not_summed = {
        'Axis': {'0': [0, 1, 2], '1': [0, 1, 2]}, 
        'Contrast': {
            '0': [
                [0.0314427347246871, 0.031350381068575774, 0.031270925007150875, 0.03120181028257687, 0.03114112018407596, 0.031087388363708293, 0.03103947220464664, 0.03099646773820117],
                [0.01823324914799796, 0.0181999942864648, 0.018171731665378766, 0.018147410904883567, 0.018126260341714225, 0.018107689874176935, 0.018091258365579566, 0.018076613742741603],
                [0.012844135035163327, 0.012827140880615486, 0.012812775377438202, 0.01280047107875312, 0.012789813347910552, 0.012780481384172395, 0.012772269375840866, 0.01276496218482732]], 
            '1': [
                [0.0314427347246871, 0.031350381068575774, 0.031270925007150875, 0.03120181028257687, 0.03114112018407596, 0.031087388363708293, 0.03103947220464664, 0.03099646773820117],
                [0.01823324914799796, 0.0181999942864648, 0.018171731665378766, 0.018147410904883567, 0.018126260341714225, 0.018107689874176935, 0.018091258365579566, 0.018076613742741603],
                [0.012844135035163327, 0.012827140880615486, 0.012812775377438202, 0.01280047107875312, 0.012789813347910552, 0.012780481384172395, 0.012772269375840866, 0.01276496218482732]]}, 
        'Contrast_error': {
            '0': [
                [1.5804937893622582e-06, 1.6285752044102746e-06, 1.6753907778514714e-06, 1.7214614488091245e-06, 1.7655585288265553e-06, 1.8090589025865455e-06, 1.8537161775668089e-06, 1.8932136038155265e-06],
                [1.6804272281913843e-06, 1.7440793366712698e-06, 1.8055523523678614e-06, 1.8650500316263587e-06, 1.9227470254303512e-06, 1.980129405320712e-06, 2.033222812910883e-06, 2.0864492586007134e-06],
                [1.7190899601904628e-06, 1.7896854801417866e-06, 1.8576380923764978e-06, 1.9232205089792115e-06, 1.986662097367915e-06, 2.0481578022752833e-06, 2.1078748928000863e-06, 2.1659581668611777e-06]],
            '1': [[1.5804937893622582e-06, 1.6285752044102746e-06, 1.6753907778514714e-06, 1.7214614488091245e-06, 1.7655585288265553e-06, 1.8090589025865455e-06, 1.8537161775668089e-06, 1.8932136038155265e-06],
                [1.6804272281913843e-06, 1.7440793366712698e-06, 1.8055523523678614e-06, 1.8650500316263587e-06, 1.9227470254303512e-06, 1.980129405320712e-06, 2.033222812910883e-06, 2.0864492586007134e-06],
                [1.7190899601904628e-06, 1.7896854801417866e-06, 1.8576380923764978e-06, 1.9232205089792115e-06, 1.986662097367915e-06, 2.0481578022752833e-06, 2.1078748928000863e-06, 2.1659581668611777e-06]]},
        'Background': None, 
        'Foil': None}

    @parameterized.expand([
        # Test the behaviour
        ('tested_summed', True, expectation_summed),
        # Test the behaviour
        ('tested_not_summed', False, expectation_not_summed)
    ])
    def test_calcContrastMain(self, _, sum_foils, expectation):
        self.contrast_proc.para_dict['sum_foils'] = sum_foils
        self.contrast_proc.calcContrastMain(
            self.target, Mock(mask=self.masks['flat']),
            self.results,
            select=['0', '1'],
            foil=None)
        self.maxDiff = None

        result = self.results.getLastResult('Contrast calculation').result_dict
        self.assertEqual(expectation, result)


class Test_calcContrastRef(unittest.TestCase):
    def setUp(self) -> None:

        # Set up the used class
        self.contrast_proc = Fit_MIEZE()
        self.contrast_proc.para_dict['foils_in_echo'] = [[1 for i in range(8)] for j in range(30)]
        self.contrast_proc.para_dict['processors'] = 1

        # Set up the fake return function for the axes
        def get_axis(axis_name):
            if axis_name == self.contrast_proc.para_dict['foil_name']:
                return [i for i in range(8)]
            if axis_name == self.contrast_proc.para_dict['meas_name']:
                return [0]
            if axis_name == self.contrast_proc.para_dict['para_name']:
                return [str(i) for i in range(2)]
            if axis_name == self.contrast_proc.para_dict['tcha_name']:
                return [i for i in range(16)]
            if axis_name == self.contrast_proc.para_dict['echo_name']:
                return [i for i in range(3)]

        # Set up the fake return function for the axis length
        def get_axis_len(axis_name):
            if axis_name == self.contrast_proc.para_dict['tcha_name']:
                return 16
            if axis_name == self.contrast_proc.para_dict['foil_name']:
                return 8
            if axis_name == self.contrast_proc.para_dict['meas_name']:
                return 1
            if axis_name == self.contrast_proc.para_dict['para_name']:
                return 2
            if axis_name == self.contrast_proc.para_dict['echo_name']:
                return 3

        names = ['Parameter', 'Measurement', 'Echo Time', 'Foil', 'Time Channel']

        # Now nock it in
        self.target = Mock(
            get_axis_len=Mock(wraps=get_axis_len),
            get_axis=Mock(wraps=get_axis),
            map=np.zeros((2, 1, 3, 1, 1), dtype=int),
            metadata_objects=[{'Monitor': 10}],
            metadata_addresses=[0],
            data_objects=[Mock(meta_address=[0])],
            axes=Mock(names=names))

        # Set up the used mask
        self.masks = {}
        self.masks['flat'] = np.ones((128, 128), dtype=np.uint32)

        # set up the used data
        self.data = {}
        self.data['sinus'] = np.zeros((2, 1, 3, 8, 16), dtype=np.uint32)
        for echo in range(3):
            for time_channel in range(16):
                value = 10000 / (echo + 1) * np.sin(np.pi * time_channel / 15) + 10000
                for foil in range(8):
                    self.data['sinus'][:, 0, echo, foil, time_channel] = value + 1000 * foil
        self.data['sinus'][0] *= 2

        self.results = ResultStructure(mode='Dict')

        local_results = self.results.generateResult(name='Contrast mode')
        local_results['Mode'] = 'Corrected'
        local_results.setComplete()

        local_results = self.results.generateResult(name='Corrected Phase')
        local_results['Shift'] = self.data['sinus']
        local_results.setComplete()

    expectation_summed = {'Reference': '0',
                          'Contrast_ref': {0: 0.37209263219565897, 1: 1.1615838600179353, 2: 1.777224782509143},
                          'Contrast_ref_error': {0: 1.3135277632258316e-05, 1: 8.432927545257018e-05,
                                                 2: 2.589879232666367e-05}}

    expectation_not_summed = {
        'Reference': '0', 
        'Contrast_ref': {
            0: [0.3067525683126683, 0.2878031073450281, 0.2710772677910944, 0.25620196340149776, 0.24288391484142974, 0.23088919408022893, 0.2200288046935244, 0.2101483143478133], 
            1: [0.1852200989937729, 0.1716506519517564, 0.15993769630341417, 0.14972387997479245, 0.14073823277617262, 0.13277142268149197, 0.1256592855507402, 0.11927112251672774], 
            2: [0.13276806382808648, 0.12237874219006352, 0.1134988186042722, 0.1058213571705122, 0.0991174272233678, 0.09321270600782729, 0.08797244022354568, 0.08329021192067632]}, 
        'Contrast_ref_error': {
            0: [1.5419159094594902e-05, 1.4950663704823493e-05, 1.45234064690609e-05, 1.4135135080645077e-05, 1.377040276098833e-05, 1.343606439933335e-05, 1.3140395948163555e-05, 1.2835515675608743e-05],
            1: [1.7070402265172535e-05, 1.6449035669085417e-05, 1.5891489545991317e-05, 1.538745821901581e-05, 1.4928838786010668e-05, 1.4518947478375543e-05, 1.4122474007775467e-05, 1.3766579774789111e-05],
            2: [1.7769997351782567e-05, 1.7074690300358073e-05, 1.645543004291564e-05, 1.5899243328329746e-05, 1.539606798761116e-05, 1.4937960890702895e-05, 1.451855520337866e-05, 1.4132679135048103e-05]}}

    @parameterized.expand([
        # Test the behaviour
        ('tested_summed', True, expectation_summed),
        # Test the behaviour
        ('tested_not_summed', False, expectation_not_summed)
    ])
    def test_calcContrastRef(self, _, sum_foils, expectation):
        self.contrast_proc.para_dict['sum_foils'] = sum_foils
        self.contrast_proc.para_dict['Reference'] = ['0', '0']
        self.contrast_proc.calcContrastRef(
            self.target,
            Mock(mask=self.masks['flat']),
            self.results)
        self.maxDiff = None

        result = self.results.getLastResult('Reference contrast calculation').result_dict
        print(result)
        self.assertEqual(expectation, result)


class Test_contrastFit(unittest.TestCase):
    def setUp(self) -> None:

        # Set up the used class
        self.contrast_proc = Fit_MIEZE()
        self.contrast_proc.para_dict['foils_in_echo'] = [[1 for i in range(8)] for j in range(30)]
        self.contrast_proc.para_dict['processors'] = 1

        # Set up the fake return function for the axes
        def get_axis(axis_name):
            if axis_name == self.contrast_proc.para_dict['foil_name']:
                return [i for i in range(8)]
            if axis_name == self.contrast_proc.para_dict['meas_name']:
                return [0]
            if axis_name == self.contrast_proc.para_dict['para_name']:
                return [str(i) for i in range(2)]
            if axis_name == self.contrast_proc.para_dict['tcha_name']:
                return [i for i in range(16)]
            if axis_name == self.contrast_proc.para_dict['echo_name']:
                return [i for i in range(3)]

        # Set up the fake return function for the axis length
        def get_axis_len(axis_name):
            if axis_name == self.contrast_proc.para_dict['tcha_name']:
                return 16
            if axis_name == self.contrast_proc.para_dict['foil_name']:
                return 8
            if axis_name == self.contrast_proc.para_dict['meas_name']:
                return 1
            if axis_name == self.contrast_proc.para_dict['para_name']:
                return 2
            if axis_name == self.contrast_proc.para_dict['echo_name']:
                return 3

        names = ['Parameter', 'Measurement', 'Echo Time', 'Foil', 'Time Channel']

        # Now nock it in
        self.target = Mock(
            get_axis_len=Mock(wraps=get_axis_len),
            get_axis=Mock(wraps=get_axis),
            map=np.zeros((2, 1, 3, 1, 1), dtype=int),
            metadata_objects=[{'Monitor': 10}],
            metadata_addresses=[0],
            data_objects=[Mock(meta_address=[0])],
            axes=Mock(names=names, units=['ns']))

        # Set up the used mask
        self.masks = {}
        self.masks['flat'] = np.ones((128, 128), dtype=np.uint32)

        # set up the used data
        self.data = {}
        self.data['sinus'] = np.zeros((2, 1, 3, 8, 16), dtype=np.uint32)
        for echo in range(3):
            for time_channel in range(16):
                value = 10000 / (echo + 1) * np.sin(np.pi * time_channel / 15) + 10000
                for foil in range(8):
                    self.data['sinus'][:, 0, echo, foil, time_channel] = value + 1000 * foil
        self.data['sinus'][0] *= 2
        self.results = ResultStructure(mode='Dict')

        local_results = self.results.generateResult(name='Contrast mode')
        local_results['Mode'] = 'Corrected'
        local_results.setComplete()

        local_results = self.results.generateResult(name='Corrected Phase')
        local_results['Shift'] = self.data['sinus']
        local_results.setComplete()


    summed_expectations = {
        'Parameters': {
            '0': {
                'x': np.array([0, 1, 2]), 
                'x_unit': 'ns', 
                'y': np.array([1., 1., 1.]), 
                'y_raw': np.array([0.37209263, 1.16158386, 1.77722478]), 
                'y_error': np.array([4.99232884e-05, 1.02669819e-04, 2.06087737e-05]),
                'y_raw_error': np.array([1.31352776e-05, 8.43292755e-05, 2.58987923e-05])},
            '1': {
                'x': np.array([0, 1, 2]),
                'x_unit': 'ns',
                'y': np.array([0.67016671, 0.12490861, 0.05759523]),
                'y_raw': np.array([0.2493641 , 0.14509183, 0.10235966]),
                'y_error': np.array([3.01817768e-05, 1.11702814e-05, 4.47515381e-06]),
                'y_raw_error': np.array([6.97370190e-06, 7.57645474e-06, 7.81222336e-06])}},
        'Select': ['0', '1'],
        'BG': None,
        'Reference': ['0', '0'],
        'Axis': {'0': [0, 1, 2], '1': [0, 1, 2]},
        'Axis_unit': 'ns',
        'Sum_Foils': True
    }

    not_summed_expectations = {
        'Parameters': {
            '0': {
                'x': np.array([0, 1, 2]),
                'x_unit': 'ns',
                'y': np.array([1., 1., 1.]),
                'y_raw': np.array([0.2495303 , 0.14515421, 0.10239205]),
                'y_error': np.array([7.86350692e-05, 1.46527978e-04, 2.14190847e-04]),
                'y_raw_error': np.array([1.39274684e-05, 1.51176575e-05, 1.55982870e-05])},
            '1': {
                'x': np.array([0, 1, 2]),
                'x_unit': 'ns',
                'y': np.array([1.        , 0.99999998, 1.00000013]),
                'y_raw': np.array([0.2495303 , 0.14515421, 0.10239206]),
                'y_error': np.array([9.64181954e-05, 1.79755032e-04, 2.62878382e-04]),
                'y_raw_error': np.array([1.96927937e-05, 2.13768470e-05, 2.20641073e-05])}},
        'Select': ['0', '1'],
        'BG': None,
        'Reference': ['0', '0'],
        'Axis': {'0': [0, 1, 2], '1': [0, 1, 2]},
        'Axis_unit': 'ns',
        'Sum_Foils': False}

    @parameterized.expand([
        # Test the behaviour
        ('tested_summed', True, summed_expectations),
        # Test the behaviour
        ('tested_not_summed', False, not_summed_expectations)
    ])
    def test_contrastFit(self, _, sum_foils, expectation):
        self.contrast_proc.para_dict['sum_foils'] = sum_foils

        self.contrast_proc.para_dict['Reference'] = ['0', '0']
        self.contrast_proc.calcContrastRef(
            self.target,
            Mock(mask=self.masks['flat']),
            self.results)

        self.contrast_proc.para_dict['Select'] = ['0', '1']
        self.contrast_proc.calcContrastMain(
            self.target, 
            Mock(mask=self.masks['flat']),
            self.results, 
            select=['0', '1'], 
            foil=None)

        self.contrast_proc.contrastFit(
            self.target, 
            Mock(mask=self.masks['flat']),
            self.results)

        self.maxDiff = None

        result = self.results.getLastResult('Contrast fit').result_dict
        self.checkNestedItems(expectation, result)

    def checkNestedItems(self, items_expectation, items_result):
        if isinstance(items_expectation, dict) and isinstance(items_result, dict):
            for key in items_expectation.keys():
                self.assertIn(key, items_result.keys())
                self.checkNestedItems(items_expectation[key], items_result[key])
        elif isinstance(items_expectation, list) and isinstance(items_result, list):
            self.assertEqual(len(items_expectation), len(items_result))
            for i in range(len(items_expectation)):
                self.checkNestedItems(items_expectation[i], items_result[i])
        elif isinstance(items_expectation, np.ndarray) and isinstance(items_result, np.ndarray):
            self.assertEqual(items_expectation.shape, items_result.shape)
            for i in range(items_expectation.shape[0]):
                self.checkNestedItems(items_expectation[i], items_result[i])
        else:
            if isinstance(items_expectation, float) and isinstance(items_result, float):
                self.assertAlmostEqual(items_expectation, items_result)
            else:
                self.assertEqual(items_expectation, items_result)
            

