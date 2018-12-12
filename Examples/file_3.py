def loadData(env, gui = None):
    if not gui == None:
        for i in range(13):
            gui.addElement()
    else:
        for i in range(13):
            env.io.addObject()
    import_result  = [None]*13
    import_result[0] = loadData_0(env.io.import_objects[0])
    import_result[1] = loadData_1(env.io.import_objects[1])
    import_result[2] = loadData_2(env.io.import_objects[2])
    import_result[3] = loadData_3(env.io.import_objects[3])
    import_result[4] = loadData_4(env.io.import_objects[4])
    import_result[5] = loadData_5(env.io.import_objects[5])
    import_result[6] = loadData_6(env.io.import_objects[6])
    import_result[7] = loadData_7(env.io.import_objects[7])
    import_result[8] = loadData_8(env.io.import_objects[8])
    import_result[9] = loadData_9(env.io.import_objects[9])
    import_result[10] = loadData_10(env.io.import_objects[10])
    import_result[11] = loadData_11(env.io.import_objects[11])
    import_result[12] = loadData_12(env.io.import_objects[12])
    passed = all([all([subelement[0] for subelement in element]) for element in import_result])
    if not gui == None:
        for i in range(13):
            gui.setCurrentElement(i)
            if passed:
                gui.populate()
    else:
        for i in range(13):
            if passed:
                env.io.import_objects[i].processObject()
    return import_result

def loadData_0(import_object):
    #################################
    ########## add element ##########
    current_object  = import_object
    meta_files_found = [True,'']
    data_files_found = [True,'']
    
    ########## The meta info ##########
    try:
        path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
        current_object.meta_handler.buildMeta(path)
        selected_meta = [
            ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
            ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
            ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
            ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
            ['monitor1' ,'m' ,'Monitor' ,'1' ]]
        current_object.meta_handler.selected_meta = selected_meta
    except:
        meta_files_found = [False,path]
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data'
    path_list = [
        '00122186.tof',
        '00122187.tof',
        '00122188.tof',
        '00122189.tof',
        '00122190.tof',
        '00122191.tof',
        '00122192.tof',
        '00122193.tof']
    if current_object.file_handler.filesExist([
        os.path.join(common_path,item) for item in path_list]):
        current_object.file_handler.addFiles([
            os.path.join(common_path,item) for item in path_list])
    else:
        data_files_found = [False,common_path]
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '68.00'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = True
    return [meta_files_found, data_files_found]

def loadData_1(import_object):
    #################################
    ########## add element ##########
    current_object  = import_object
    meta_files_found = [True,'']
    data_files_found = [True,'']
    
    ########## The meta info ##########
    try:
        path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
        current_object.meta_handler.buildMeta(path)
        selected_meta = [
            ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
            ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
            ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
            ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
            ['monitor1' ,'m' ,'Monitor' ,'1' ]]
        current_object.meta_handler.selected_meta = selected_meta
    except:
        meta_files_found = [False,path]
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data'
    path_list = [
        '00122387.tof',
        '00122388.tof',
        '00122389.tof',
        '00122390.tof',
        '00122391.tof',
        '00122392.tof',
        '00122393.tof',
        '00122394.tof']
    if current_object.file_handler.filesExist([
        os.path.join(common_path,item) for item in path_list]):
        current_object.file_handler.addFiles([
            os.path.join(common_path,item) for item in path_list])
    else:
        data_files_found = [False,common_path]
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '31.00'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False
    return [meta_files_found, data_files_found]

def loadData_2(import_object):
    #################################
    ########## add element ##########
    current_object  = import_object
    meta_files_found = [True,'']
    data_files_found = [True,'']
    
    ########## The meta info ##########
    try:
        path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
        current_object.meta_handler.buildMeta(path)
        selected_meta = [
            ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
            ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
            ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
            ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
            ['monitor1' ,'m' ,'Monitor' ,'1' ]]
        current_object.meta_handler.selected_meta = selected_meta
    except:
        meta_files_found = [False,path]
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data'
    path_list = [
        '00122396.tof',
        '00122398.tof',
        '00122401.tof',
        '00122402.tof',
        '00122403.tof']
    if current_object.file_handler.filesExist([
        os.path.join(common_path,item) for item in path_list]):
        current_object.file_handler.addFiles([
            os.path.join(common_path,item) for item in path_list])
    else:
        data_files_found = [False,common_path]
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '30.00'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False
    return [meta_files_found, data_files_found]

def loadData_3(import_object):
    #################################
    ########## add element ##########
    current_object  = import_object
    meta_files_found = [True,'']
    data_files_found = [True,'']
    
    ########## The meta info ##########
    try:
        path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
        current_object.meta_handler.buildMeta(path)
        selected_meta = [
            ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
            ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
            ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
            ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
            ['monitor1' ,'m' ,'Monitor' ,'1' ]]
        current_object.meta_handler.selected_meta = selected_meta
    except:
        meta_files_found = [False,path]
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data'
    path_list = [
        '00122408.tof',
        '00122409.tof',
        '00122410.tof']
    if current_object.file_handler.filesExist([
        os.path.join(common_path,item) for item in path_list]):
        current_object.file_handler.addFiles([
            os.path.join(common_path,item) for item in path_list])
    else:
        data_files_found = [False,common_path]
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '30.00'
    current_object.data_handler.meas = '1'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False
    return [meta_files_found, data_files_found]

def loadData_4(import_object):
    #################################
    ########## add element ##########
    current_object  = import_object
    meta_files_found = [True,'']
    data_files_found = [True,'']
    
    ########## The meta info ##########
    try:
        path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
        current_object.meta_handler.buildMeta(path)
        selected_meta = [
            ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
            ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
            ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
            ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
            ['monitor1' ,'m' ,'Monitor' ,'1' ]]
        current_object.meta_handler.selected_meta = selected_meta
    except:
        meta_files_found = [False,path]
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data'
    path_list = [
        '00122412.tof',
        '00122413.tof',
        '00122374.tof',
        '00122375.tof',
        '00122376.tof',
        '00122377.tof',
        '00122378.tof',
        '00122379.tof']
    if current_object.file_handler.filesExist([
        os.path.join(common_path,item) for item in path_list]):
        current_object.file_handler.addFiles([
            os.path.join(common_path,item) for item in path_list])
    else:
        data_files_found = [False,common_path]
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '29.80'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False
    return [meta_files_found, data_files_found]

def loadData_5(import_object):
    #################################
    ########## add element ##########
    current_object  = import_object
    meta_files_found = [True,'']
    data_files_found = [True,'']
    
    ########## The meta info ##########
    try:
        path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
        current_object.meta_handler.buildMeta(path)
        selected_meta = [
            ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
            ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
            ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
            ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
            ['monitor1' ,'m' ,'Monitor' ,'1' ]]
        current_object.meta_handler.selected_meta = selected_meta
    except:
        meta_files_found = [False,path]
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data'
    path_list = [
        '00122320.tof',
        '00122321.tof',
        '00122414.tof',
        '00122323.tof',
        '00122415.tof',
        '00122325.tof',
        '00122326.tof',
        '00122327.tof']
    if current_object.file_handler.filesExist([
        os.path.join(common_path,item) for item in path_list]):
        current_object.file_handler.addFiles([
            os.path.join(common_path,item) for item in path_list])
    else:
        data_files_found = [False,common_path]
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '29.60'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False
    return [meta_files_found, data_files_found]

def loadData_6(import_object):
    #################################
    ########## add element ##########
    current_object  = import_object
    meta_files_found = [True,'']
    data_files_found = [True,'']
    
    ########## The meta info ##########
    try:
        path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
        current_object.meta_handler.buildMeta(path)
        selected_meta = [
            ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
            ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
            ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
            ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
            ['monitor1' ,'m' ,'Monitor' ,'1' ]]
        current_object.meta_handler.selected_meta = selected_meta
    except:
        meta_files_found = [False,path]
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data'
    path_list = [
        '00122334.tof',
        '00122335.tof',
        '00122336.tof',
        '00122337.tof',
        '00122338.tof',
        '00122339.tof',
        '00122340.tof',
        '00122341.tof']
    if current_object.file_handler.filesExist([
        os.path.join(common_path,item) for item in path_list]):
        current_object.file_handler.addFiles([
            os.path.join(common_path,item) for item in path_list])
    else:
        data_files_found = [False,common_path]
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '29.40'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False
    return [meta_files_found, data_files_found]

def loadData_7(import_object):
    #################################
    ########## add element ##########
    current_object  = import_object
    meta_files_found = [True,'']
    data_files_found = [True,'']
    
    ########## The meta info ##########
    try:
        path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
        current_object.meta_handler.buildMeta(path)
        selected_meta = [
            ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
            ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
            ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
            ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
            ['monitor1' ,'m' ,'Monitor' ,'1' ]]
        current_object.meta_handler.selected_meta = selected_meta
    except:
        meta_files_found = [False,path]
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data'
    path_list = [
        '00122348.tof',
        '00122349.tof',
        '00122350.tof',
        '00122351.tof',
        '00122352.tof',
        '00122353.tof',
        '00122354.tof']
    if current_object.file_handler.filesExist([
        os.path.join(common_path,item) for item in path_list]):
        current_object.file_handler.addFiles([
            os.path.join(common_path,item) for item in path_list])
    else:
        data_files_found = [False,common_path]
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '29.20'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False
    return [meta_files_found, data_files_found]

def loadData_8(import_object):
    #################################
    ########## add element ##########
    current_object  = import_object
    meta_files_found = [True,'']
    data_files_found = [True,'']
    
    ########## The meta info ##########
    try:
        path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
        current_object.meta_handler.buildMeta(path)
        selected_meta = [
            ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
            ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
            ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
            ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
            ['monitor1' ,'m' ,'Monitor' ,'1' ]]
        current_object.meta_handler.selected_meta = selected_meta
    except:
        meta_files_found = [False,path]
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data'
    path_list = [
        '00122416.tof']
    if current_object.file_handler.filesExist([
        os.path.join(common_path,item) for item in path_list]):
        current_object.file_handler.addFiles([
            os.path.join(common_path,item) for item in path_list])
    else:
        data_files_found = [False,common_path]
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '29.20'
    current_object.data_handler.meas = '1'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False
    return [meta_files_found, data_files_found]

def loadData_9(import_object):
    #################################
    ########## add element ##########
    current_object  = import_object
    meta_files_found = [True,'']
    data_files_found = [True,'']
    
    ########## The meta info ##########
    try:
        path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
        current_object.meta_handler.buildMeta(path)
        selected_meta = [
            ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
            ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
            ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
            ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
            ['monitor1' ,'m' ,'Monitor' ,'1' ]]
        current_object.meta_handler.selected_meta = selected_meta
    except:
        meta_files_found = [False,path]
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data'
    path_list = [
        '00122418.tof',
        '00122419.tof',
        '00122420.tof',
        '00122421.tof',
        '00122422.tof',
        '00122423.tof',
        '00122424.tof',
        '00122425.tof']
    if current_object.file_handler.filesExist([
        os.path.join(common_path,item) for item in path_list]):
        current_object.file_handler.addFiles([
            os.path.join(common_path,item) for item in path_list])
    else:
        data_files_found = [False,common_path]
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '29.10'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False
    return [meta_files_found, data_files_found]

def loadData_10(import_object):
    #################################
    ########## add element ##########
    current_object  = import_object
    meta_files_found = [True,'']
    data_files_found = [True,'']
    
    ########## The meta info ##########
    try:
        path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
        current_object.meta_handler.buildMeta(path)
        selected_meta = [
            ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
            ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
            ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
            ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
            ['monitor1' ,'m' ,'Monitor' ,'1' ]]
        current_object.meta_handler.selected_meta = selected_meta
    except:
        meta_files_found = [False,path]
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data'
    path_list = [
        '00122362.tof',
        '00122363.tof',
        '00122364.tof',
        '00122365.tof',
        '00122366.tof',
        '00122426.tof',
        '00122368.tof',
        '00122369.tof']
    if current_object.file_handler.filesExist([
        os.path.join(common_path,item) for item in path_list]):
        current_object.file_handler.addFiles([
            os.path.join(common_path,item) for item in path_list])
    else:
        data_files_found = [False,common_path]
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '29.00'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False
    return [meta_files_found, data_files_found]

def loadData_11(import_object):
    #################################
    ########## add element ##########
    current_object  = import_object
    meta_files_found = [True,'']
    data_files_found = [True,'']
    
    ########## The meta info ##########
    try:
        path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
        current_object.meta_handler.buildMeta(path)
        selected_meta = [
            ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
            ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
            ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
            ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
            ['monitor1' ,'m' ,'Monitor' ,'1' ]]
        current_object.meta_handler.selected_meta = selected_meta
    except:
        meta_files_found = [False,path]
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data'
    path_list = [
        '00122434.tof',
        '00122435.tof',
        '00122436.tof',
        '00122437.tof',
        '00122438.tof',
        '00122439.tof',
        '00122440.tof',
        '00122441.tof']
    if current_object.file_handler.filesExist([
        os.path.join(common_path,item) for item in path_list]):
        current_object.file_handler.addFiles([
            os.path.join(common_path,item) for item in path_list])
    else:
        data_files_found = [False,common_path]
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '28.60'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = False
    current_object.data_handler.background = False
    return [meta_files_found, data_files_found]

def loadData_12(import_object):
    #################################
    ########## add element ##########
    current_object  = import_object
    meta_files_found = [True,'']
    data_files_found = [True,'']
    
    ########## The meta info ##########
    try:
        path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof'
        current_object.meta_handler.buildMeta(path)
        selected_meta = [
            ['cbox_0a_fg_freq_value' ,'Hz' ,'Freq. first' ,'1' ],
            ['cbox_0b_fg_freq_value' ,'Hz' ,'Freq. second' ,'1' ],
            ['selector_lambda_value' ,'A' ,'Wavelength' ,'1.e-10' ],
            ['psd_distance_value' ,'m' ,'lsd' ,'1.e9 ' ],
            ['monitor1' ,'m' ,'Monitor' ,'1' ]]
        current_object.meta_handler.selected_meta = selected_meta
    except:
        meta_files_found = [False,path]
    
    ########## The file paths ##########
    common_path = '/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data'
    path_list = [
        '00122306.tof',
        '00122307.tof',
        '00122308.tof',
        '00122309.tof',
        '00122310.tof',
        '00122311.tof',
        '00122312.tof',
        '00122313.tof']
    if current_object.file_handler.filesExist([
        os.path.join(common_path,item) for item in path_list]):
        current_object.file_handler.addFiles([
            os.path.join(common_path,item) for item in path_list])
    else:
        data_files_found = [False,common_path]
    ########## The data handler ##########
    current_object.data_handler.dimension = [8, 16, 128, 128]
    current_object.data_handler.parameter = '28.40'
    current_object.data_handler.meas = '0'
    current_object.data_handler.reference = True
    current_object.data_handler.background = False
    return [meta_files_found, data_files_found]
