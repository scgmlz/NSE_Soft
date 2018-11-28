def loadData(env, gui = None):
    if not gui == None:
        for i in range(13):
            gui.addElement()
    else:
        for i in range(13):
            env.io.addObject()
    loadData_0(env.io.import_objects[0])
    loadData_1(env.io.import_objects[1])
    loadData_2(env.io.import_objects[2])
    loadData_3(env.io.import_objects[3])
    loadData_4(env.io.import_objects[4])
    loadData_5(env.io.import_objects[5])
    loadData_6(env.io.import_objects[6])
    loadData_7(env.io.import_objects[7])
    loadData_8(env.io.import_objects[8])
    loadData_9(env.io.import_objects[9])
    loadData_10(env.io.import_objects[10])
    loadData_11(env.io.import_objects[11])
    loadData_12(env.io.import_objects[12])
    if not gui == None:
        for i in range(13):
            gui.setCurrentElement(i)
            gui.populate()
    else:
        for i in range(13):
            env.io.import_objects[i].processObject()

def loadData_0(import_object):
    #################################
    ########## add element ##########
    current_object = import_object
    
    ########## The meta info ##########
    path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
    current_object.meta_handler.buildMeta(path)
    selected_meta = [
        ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
        ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
        ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
        ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
        ['monitor1' ,'m' ,'Monitor' ,'1' ]]
    current_object.meta_handler.selected_meta = selected_meta
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/001221'
    path_list = [
        '86.tof',
        '87.tof',
        '88.tof',
        '89.tof',
        '90.tof',
        '91.tof',
        '92.tof',
        '93.tof']
    current_object.file_handler.addFiles([
        common_path + item for item in path_list])
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '68.00'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = True

def loadData_1(import_object):
    #################################
    ########## add element ##########
    current_object = import_object
    
    ########## The meta info ##########
    path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
    current_object.meta_handler.buildMeta(path)
    selected_meta = [
        ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
        ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
        ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
        ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
        ['monitor1' ,'m' ,'Monitor' ,'1' ]]
    current_object.meta_handler.selected_meta = selected_meta
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/001223'
    path_list = [
        '87.tof',
        '88.tof',
        '89.tof',
        '90.tof',
        '91.tof',
        '92.tof',
        '93.tof',
        '94.tof']
    current_object.file_handler.addFiles([
        common_path + item for item in path_list])
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '31.00'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False

def loadData_2(import_object):
    #################################
    ########## add element ##########
    current_object = import_object
    
    ########## The meta info ##########
    path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
    current_object.meta_handler.buildMeta(path)
    selected_meta = [
        ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
        ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
        ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
        ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
        ['monitor1' ,'m' ,'Monitor' ,'1' ]]
    current_object.meta_handler.selected_meta = selected_meta
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122'
    path_list = [
        '396.tof',
        '398.tof',
        '401.tof',
        '402.tof',
        '403.tof']
    current_object.file_handler.addFiles([
        common_path + item for item in path_list])
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '30.00'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False

def loadData_3(import_object):
    #################################
    ########## add element ##########
    current_object = import_object
    
    ########## The meta info ##########
    path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
    current_object.meta_handler.buildMeta(path)
    selected_meta = [
        ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
        ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
        ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
        ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
        ['monitor1' ,'m' ,'Monitor' ,'1' ]]
    current_object.meta_handler.selected_meta = selected_meta
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/001224'
    path_list = [
        '08.tof',
        '09.tof',
        '10.tof']
    current_object.file_handler.addFiles([
        common_path + item for item in path_list])
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '30.00'
    current_object.data_handler.meas = '1'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False

def loadData_4(import_object):
    #################################
    ########## add element ##########
    current_object = import_object
    
    ########## The meta info ##########
    path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
    current_object.meta_handler.buildMeta(path)
    selected_meta = [
        ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
        ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
        ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
        ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
        ['monitor1' ,'m' ,'Monitor' ,'1' ]]
    current_object.meta_handler.selected_meta = selected_meta
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122'
    path_list = [
        '412.tof',
        '413.tof',
        '374.tof',
        '375.tof',
        '376.tof',
        '377.tof',
        '378.tof',
        '379.tof']
    current_object.file_handler.addFiles([
        common_path + item for item in path_list])
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '29.80'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False

def loadData_5(import_object):
    #################################
    ########## add element ##########
    current_object = import_object
    
    ########## The meta info ##########
    path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
    current_object.meta_handler.buildMeta(path)
    selected_meta = [
        ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
        ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
        ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
        ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
        ['monitor1' ,'m' ,'Monitor' ,'1' ]]
    current_object.meta_handler.selected_meta = selected_meta
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122'
    path_list = [
        '320.tof',
        '321.tof',
        '414.tof',
        '323.tof',
        '415.tof',
        '325.tof',
        '326.tof',
        '327.tof']
    current_object.file_handler.addFiles([
        common_path + item for item in path_list])
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '29.60'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False

def loadData_6(import_object):
    #################################
    ########## add element ##########
    current_object = import_object
    
    ########## The meta info ##########
    path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
    current_object.meta_handler.buildMeta(path)
    selected_meta = [
        ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
        ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
        ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
        ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
        ['monitor1' ,'m' ,'Monitor' ,'1' ]]
    current_object.meta_handler.selected_meta = selected_meta
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/001223'
    path_list = [
        '34.tof',
        '35.tof',
        '36.tof',
        '37.tof',
        '38.tof',
        '39.tof',
        '40.tof',
        '41.tof']
    current_object.file_handler.addFiles([
        common_path + item for item in path_list])
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '29.40'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False

def loadData_7(import_object):
    #################################
    ########## add element ##########
    current_object = import_object
    
    ########## The meta info ##########
    path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
    current_object.meta_handler.buildMeta(path)
    selected_meta = [
        ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
        ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
        ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
        ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
        ['monitor1' ,'m' ,'Monitor' ,'1' ]]
    current_object.meta_handler.selected_meta = selected_meta
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/001223'
    path_list = [
        '48.tof',
        '49.tof',
        '50.tof',
        '51.tof',
        '52.tof',
        '53.tof',
        '54.tof']
    current_object.file_handler.addFiles([
        common_path + item for item in path_list])
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '29.20'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False

def loadData_8(import_object):
    #################################
    ########## add element ##########
    current_object = import_object
    
    ########## The meta info ##########
    path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
    current_object.meta_handler.buildMeta(path)
    selected_meta = [
        ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
        ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
        ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
        ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
        ['monitor1' ,'m' ,'Monitor' ,'1' ]]
    current_object.meta_handler.selected_meta = selected_meta
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122416.tof'
    path_list = [
        '']
    current_object.file_handler.addFiles([
        common_path + item for item in path_list])
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '29.20'
    current_object.data_handler.meas = '1'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False

def loadData_9(import_object):
    #################################
    ########## add element ##########
    current_object = import_object
    
    ########## The meta info ##########
    path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
    current_object.meta_handler.buildMeta(path)
    selected_meta = [
        ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
        ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
        ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
        ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
        ['monitor1' ,'m' ,'Monitor' ,'1' ]]
    current_object.meta_handler.selected_meta = selected_meta
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/001224'
    path_list = [
        '18.tof',
        '19.tof',
        '20.tof',
        '21.tof',
        '22.tof',
        '23.tof',
        '24.tof',
        '25.tof']
    current_object.file_handler.addFiles([
        common_path + item for item in path_list])
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '29.10'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False

def loadData_10(import_object):
    #################################
    ########## add element ##########
    current_object = import_object
    
    ########## The meta info ##########
    path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
    current_object.meta_handler.buildMeta(path)
    selected_meta = [
        ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
        ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
        ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
        ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
        ['monitor1' ,'m' ,'Monitor' ,'1' ]]
    current_object.meta_handler.selected_meta = selected_meta
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122'
    path_list = [
        '362.tof',
        '363.tof',
        '364.tof',
        '365.tof',
        '366.tof',
        '426.tof',
        '368.tof',
        '369.tof']
    current_object.file_handler.addFiles([
        common_path + item for item in path_list])
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '29.00'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False

def loadData_11(import_object):
    #################################
    ########## add element ##########
    current_object = import_object
    
    ########## The meta info ##########
    path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
    current_object.meta_handler.buildMeta(path)
    selected_meta = [
        ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
        ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
        ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
        ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
        ['monitor1' ,'m' ,'Monitor' ,'1' ]]
    current_object.meta_handler.selected_meta = selected_meta
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/001224'
    path_list = [
        '34.tof',
        '35.tof',
        '36.tof',
        '37.tof',
        '38.tof',
        '39.tof',
        '40.tof',
        '41.tof']
    current_object.file_handler.addFiles([
        common_path + item for item in path_list])
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '28.60'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False

def loadData_12(import_object):
    #################################
    ########## add element ##########
    current_object = import_object
    
    ########## The meta info ##########
    path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
    current_object.meta_handler.buildMeta(path)
    selected_meta = [
        ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
        ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
        ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
        ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
        ['monitor1' ,'m' ,'Monitor' ,'1' ]]
    current_object.meta_handler.selected_meta = selected_meta
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/001223'
    path_list = [
        '06.tof',
        '07.tof',
        '08.tof',
        '09.tof',
        '10.tof',
        '11.tof',
        '12.tof',
        '13.tof']
    current_object.file_handler.addFiles([
        common_path + item for item in path_list])
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '28.40'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = True
    current_object.data_handler.background = False
