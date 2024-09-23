#!/usr/bin/env python3
from pbxproj import XcodeProject

pbxproj_path = 'ios/NewExpensify.xcodeproj/project.pbxproj'
target_names = ['NewExpensify', 'NotificationServiceExtension']
team_id = '59DW8U4YZY'
my_id = 'jt'
bundle_id_prefix = f'me.{my_id}.'
display_name = f'({my_id}) New Expensify'

project = XcodeProject.load(pbxproj_path)

def del_key(obj, key):
    try:
        del obj[key]
    except AttributeError:
        pass

def fix_target_by_name(target_name):
    target = project.get_target_by_name(target_name)
    build_configuration_ids = project.get_object(target.buildConfigurationList).buildConfigurations

    for build_configuration_id in build_configuration_ids:
        build_configuration = project.get_object(build_configuration_id)

        build_settings = build_configuration.buildSettings

        old_bundle_id = build_settings.PRODUCT_BUNDLE_IDENTIFIER 
        old_product_name = build_settings.PRODUCT_NAME

        del_key(build_settings, 'CODE_SIGN_IDENTITY[sdk=iphoneos*]')
        del_key(build_settings, 'DEVELOPMENT_TEAM[sdk=iphoneos*]')
        del_key(build_settings, 'PROVISIONING_PROFILE_SPECIFIER[sdk=iphoneos*]')

        build_settings.CODE_SIGN_STYLE = 'Automatic'
        build_settings.CODE_SIGN_IDENTITY = 'Apple Development'
        build_settings.DEVELOPMENT_TEAM = team_id
        build_settings.PROVISIONING_PROFILE_SPECIFIER = ''
        build_settings.PRODUCT_BUNDLE_IDENTIFIER = bundle_id_prefix + old_bundle_id
        build_settings.PRODUCT_NAME = f'({my_id}) {old_product_name}'


for target_name in target_names:
    fix_target_by_name(target_name)

project.save()
