import pytest
from src.datetime_matcher import DatetimeMatcher

def test_sanity_sub(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_JPEG_FILE'))
    search_dfregex = test_pipeline['dfregex']
    replacement = r'%Y%m%d-\1.jpg'
    text = r'MyLovelyPicture%38E7F8AEA5_2020-Mar-10.jpeg'
    expected_out = '20200310-MyLovelyPicture.jpg'
    # When
    actual_out = DatetimeMatcher().sub(search_dfregex, replacement, text)
    # Then
    assert actual_out == expected_out

def test_sub__no_match__text_unchanged(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_JPEG_FILE'))
    search_dfregex = test_pipeline['dfregex']
    replacement = r'%Y%m%d-\1.jpg'
    text = r'MyLovelyPicture_2020-Mar-10.jpeg'
    # When
    actual_out = DatetimeMatcher().sub(search_dfregex, replacement, text)
    # Then
    assert actual_out == text

def test_sub__many_matches__subs_all():
    # Given
    search_dfregex = r'\s*(\d+)\s*\=\>\s*%Y,?'
    replacement = r' \1 = %y;'
    text = r'January 1997: Do some stuff for each of these years.. 1 => 1970, 2 => 1971, 3 =>1972, 4 => 1973,5=>  1974'
    expected_out = r'January 1997: Do some stuff for each of these years.. 1 = 70; 2 = 71; 3 = 72; 4 = 73; 5 = 74;'
    # When
    actual_out = DatetimeMatcher().sub(search_dfregex, replacement, text)
    # Then
    assert actual_out == expected_out
