from helperFunctions import *


languages = ["en-GB_CharlotteV3Voice", "en-GB_JamesV3Voice", "en-GB_KateV3Voice", "en-US_AllisonV3Voice", "en-US_EmilyV3Voice", "en-US_HenryV3Voice", "en-US_KevinV3Voice", "en-US_LisaV3Voice", "en-US_MichaelV3Voice", "en-US_OliviaV3Voice", "fr-CA_LouiseV3Voice", "fr-FR_NicolasV3Voice", "fr-FR_ReneeV3Voice", "it-IT_FrancescaV3Voice"]
texts = "Hello world, I am from IBM Watson Text-to-Speech Library."
name = "test_1.wav"

def tts_testing(text, file_name, language):
    text_to_speech(text, file_name, language)

tts_testing(texts, name, languages[6])
