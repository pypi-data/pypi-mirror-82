"""Auto-generated file, do not edit by hand. IE metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_IE = PhoneMetadata(id='IE', country_code=353, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='(?:1\\d|[2569])\\d{6,8}|4\\d{6,9}|7\\d{8}|8\\d{8,9}', possible_length=(7, 8, 9, 10), possible_length_local_only=(5, 6)),
    fixed_line=PhoneNumberDesc(national_number_pattern='(?:1\\d|21)\\d{6,7}|(?:2[24-9]|4(?:0[24]|5\\d|7)|5(?:0[45]|1\\d|8)|6(?:1\\d|[237-9])|9(?:1\\d|[35-9]))\\d{5}|(?:23|4(?:[1-469]|8\\d)|5[23679]|6[4-6]|7[14]|9[04])\\d{7}', example_number='2212345', possible_length=(7, 8, 9, 10), possible_length_local_only=(5, 6)),
    mobile=PhoneNumberDesc(national_number_pattern='8(?:22|[35-9]\\d)\\d{6}', example_number='850123456', possible_length=(9,)),
    toll_free=PhoneNumberDesc(national_number_pattern='1800\\d{6}', example_number='1800123456', possible_length=(10,)),
    premium_rate=PhoneNumberDesc(national_number_pattern='15(?:1[2-8]|[2-8]0|9[089])\\d{6}', example_number='1520123456', possible_length=(10,)),
    shared_cost=PhoneNumberDesc(national_number_pattern='18[59]0\\d{6}', example_number='1850123456', possible_length=(10,)),
    personal_number=PhoneNumberDesc(national_number_pattern='700\\d{6}', example_number='700123456', possible_length=(9,)),
    voip=PhoneNumberDesc(national_number_pattern='76\\d{7}', example_number='761234567', possible_length=(9,)),
    uan=PhoneNumberDesc(national_number_pattern='818\\d{6}', example_number='818123456', possible_length=(9,)),
    voicemail=PhoneNumberDesc(national_number_pattern='88210[1-9]\\d{4}|8(?:[35-79]5\\d\\d|8(?:[013-9]\\d\\d|2(?:[01][1-9]|[2-9]\\d)))\\d{5}', example_number='8551234567', possible_length=(10,)),
    no_international_dialling=PhoneNumberDesc(national_number_pattern='18[59]0\\d{6}', possible_length=(10,)),
    national_prefix='0',
    national_prefix_for_parsing='0',
    number_format=[NumberFormat(pattern='(\\d{2})(\\d{5})', format='\\1 \\2', leading_digits_pattern=['2[24-9]|47|58|6[237-9]|9[35-9]'], national_prefix_formatting_rule='(0\\1)'),
        NumberFormat(pattern='(\\d{3})(\\d{5})', format='\\1 \\2', leading_digits_pattern=['[45]0'], national_prefix_formatting_rule='(0\\1)'),
        NumberFormat(pattern='(\\d)(\\d{3,4})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['1'], national_prefix_formatting_rule='(0\\1)'),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{3,4})', format='\\1 \\2 \\3', leading_digits_pattern=['[2569]|4[1-69]|7[14]'], national_prefix_formatting_rule='(0\\1)'),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['70'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['81'], national_prefix_formatting_rule='(0\\1)'),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['[78]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{4})(\\d{3})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['1']),
        NumberFormat(pattern='(\\d{2})(\\d{4})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['4'], national_prefix_formatting_rule='(0\\1)'),
        NumberFormat(pattern='(\\d{2})(\\d)(\\d{3})(\\d{4})', format='\\1 \\2 \\3 \\4', leading_digits_pattern=['8'], national_prefix_formatting_rule='0\\1')],
    mobile_number_portable_region=True)
