from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, BooleanField, SubmitField, DecimalField, RadioField, DecimalField, TextField, PasswordField
from wtforms import validators
from wtforms.fields.simple import PasswordField
from wtforms.i18n import messages_path
from wtforms.validators import DataRequired, Length, NumberRange, Email, InputRequired, EqualTo


class ScenarioForm(FlaskForm):
    choices_network = [(0,'Choose network type'), ('Wi-Fi 802.11ac', 'Wi-Fi 802.11ac'), ('Wi-Fi 802.11ax', 'Wi-Fi 802.11ax'), ('LoRaWAN', 'LoRaWAN')] 
    choices_MCS = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),('5', '5'),('6', '6'),('7', '7'),('8', '8'),
                    ('9', '9'),('10', '10'),('11', '11'),('12','Ideal Wi-Fi manager')]
    #choices_bandwidth = [(20, '20'),(40, '40'),(80, '80'),(160, '160')]
    choices_spatial_streams = [('1', '1'), ('2', '2'),('4', '4')]
    choices_sf = [('0','LoRaWAN manager'), ('7','7'), ('8','8'), ('9','9'), ('10','10'), ('11','11'), ('12','12')]
    choices_prop_delay = [(0,'ConstantSpeedPropagationDelayModel'), (1,'RandomPropagationDelayModel')]
    choices_prop_loss = [(0,'Cost231PropagationLossModel'), (1,'FixedRssLossModel'), (2,'FriisPropagationLossModel'), (3,'ItuR1411LosPropagationLossModel')
                        ,(4,'ItuR1411NlosOverRooftopPropagationLossModel'), (5,'JakesPropagationLossModel'), (6,'Kun2600MhzPropagationLossModel'), (7,'LogDistancePropagationLossModel')
                        ,(8,'MatrixPropagationLossModel'), (9,'NakagamiPropagationLossModel'), (10,'OkumuraHataPropagationLossModel'), (11,'RandomPropagationLossModel'), (12,'RangePropagationLossModel')
                        ,(13,'ThreeLogDistancePropagationLossModel'), (14,'TwoRayGroundPropagationLossModel')]

    network = SelectField('Type of network', choices=choices_network)
    traffic_dir = SelectField('Traffic direction', choices=[(0,'Choose traffic direction'),('upstream','Upstream'),('downstream', 'Downstream')], validators=[DataRequired()]) 
    traffic_profile = SelectField('Traffic profile', choices=[(0,'Choose traffic profile'),('periodic','Periodic'),('cbr','CBR'),('vbr','VBR')], validators=[DataRequired()])
    packet_size_wifi = IntegerField('Packet size, bytes', validators=[DataRequired(), NumberRange(min=1,max=1500,message='A packet size must be between 1 and 1500 bytes.')],default=1024)
    packet_size_lorawan = IntegerField('Packet size, bytes', validators=[DataRequired(), NumberRange(min=1,max=230,message='A packet size must be between 1 and 230 bytes.')], default=23)
    load_freq = DecimalField('Packet period, seconds', validators=[DataRequired(), NumberRange(min=0, message='A load frequency must not be negative.')], default=1)
    mean_load = IntegerField('Mean load, Mbps', validators=[DataRequired(), NumberRange(min=0, message='A mean load must not be negative.')], default=2)
    fps = IntegerField('FPS, Frames per Second', validators=[DataRequired(), NumberRange(min=0, message='FPS must not be negative.')], default=30)
    num_devices = IntegerField('Number of end-devices', validators=[DataRequired(), NumberRange(min=1, message='A number of devices must not be negative.')]) 
    dist_devices_gateway = IntegerField('Distance end-devices-gateway, meter', validators=[DataRequired()])
    simulation_time = IntegerField('Simulation time, seconds', validators=[DataRequired(), NumberRange(min=5, message='Time must be > 5s')])
    hidden_devices = RadioField('Hidden devices?', choices = [('1', 'Yes'), ('0', 'No')], default='0')
    sf = SelectField('Spreading factor (SF)',choices= choices_sf, default='0')
    change = BooleanField('Change advanced parameters', default=0)
    prop_delay = SelectField('Propagation Delay Model', choices = choices_prop_delay, default=0, coerce=int)
    prop_loss = SelectField('Propagation Loss Model', choices = choices_prop_loss, default=7, coerce=int)
    cyclic_redundacy_check = SelectField('Cyclic Redundacy Check', choices = [('Enabled', 'Enabled'), ('Disabled','Disabled')], default='Enabled') 
    low_data_rate_optimization = SelectField('Low Data Rate Optimization', choices = [('Enabled', 'Enabled'), ('Disabled','Disabled')], default='Disabled') 
    implicit_header_mode = SelectField('Implicit Header Mode', choices = [('Enabled', 'Enabled'), ('Disabled','Disabled')], default='Disabled')
    mcs = SelectField('MCS', choices=choices_MCS, default='12')
    bandwidth = SelectField('Bandwidth', choices=[])
    spatial_streams = SelectField('Spatial streams', choices=choices_spatial_streams, default='1')
    tx = DecimalField('Tx, watts', validators=[DataRequired(), NumberRange(min=0, message='Tx must not be negative.')], default=0.52)
    rx = DecimalField('Rx, watts', validators=[DataRequired(), NumberRange(min=0, message='Rx must not be negative.')], default=0.16)
    tx_factor = DecimalField('Tx X-factor, mJ',validators=[DataRequired(), NumberRange(min=0, message='Tx X factor must not be negative.')], default=0.93)
    rx_factor = DecimalField('Rx X-factor, mJ',validators=[DataRequired(), NumberRange(min=0, message='Rx X factor must not be negative.')], default=0.93)
    voltage = DecimalField('Voltage, volts',validators=[DataRequired(), NumberRange(min=0, message='Voltage must not be negative.')], default=12)
    battery_cap = IntegerField('Battery capacity, mAh',validators=[DataRequired(), NumberRange(min=0, message='A battery ca must not be negative.')], default=5200)
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = TextField('Username', validators=[DataRequired(), Length(max=20)])
    email = TextField('Email', validators=[InputRequired(), Email(message="Invalid email!"), Length(max=100)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, message='Password must be at least 8 characters.')])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Both password fields must be match!')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = TextField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [InputRequired()])
    submit = SubmitField('Submit')