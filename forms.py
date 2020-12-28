from flask_wtf import FlaskForm
from flask_wtf import Form
from wtforms import StringField, TextField, SubmitField, IntegerField, TextAreaField, RadioField, SelectField, DecimalField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import ValidationError


class PredictForm(FlaskForm):
    MEAN_RR = DecimalField('MEAN_RR')
    MEDIAN_RR = DecimalField('MEDIAN_RR')
    SDRR = DecimalField('SDRR')
    RMSSD = DecimalField('RMSSD')
    SDSD = DecimalField('SDSD')
    SDRR_RMSSD = DecimalField('SDRR_RMSSD')
    HR = DecimalField('HR')
    pNN25 = DecimalField('pNN25')
    pNN50 = DecimalField('pNN50')
    SD1 = DecimalField('SD1')
    SD2 = DecimalField('SD2')
    KURT = DecimalField('KURT')
    SKEW = DecimalField('SKEW')
    MEAN_REL_RR = DecimalField('MEAN_REL_RR')
    MEDIAN_REL_RR = DecimalField('MEDIAN_REL_RR')
    SDRR_REL_RR = DecimalField('SDRR_REL_RR')
    RMSSD_REL_RR = DecimalField('RMSSD_REL_RR')
    SDSD_REL_RR = DecimalField('SDSD_REL_RR')
    SDRR_RMSSD_REL_RR = DecimalField('SDRR_RMSSD_REL_RR')
    KURT_REL_RR = DecimalField('KURT_REL_RR')
    SKEW_REL_RR = DecimalField('SKEW_REL_RR')
    VLF = DecimalField('VLF')
    LF = DecimalField('LF')
    HF = DecimalField('HF')
    LF_HF = DecimalField('LF_HF')
    HF_LF = DecimalField('HF_LF')
    abc = ""  # this variable is used to send information back to the front page
