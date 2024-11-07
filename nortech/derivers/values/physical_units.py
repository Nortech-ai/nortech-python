from pint import UnitRegistry

from nortech.derivers.values.physical_units_schema import (
    PhysicalQuantity,
    PhysicalUnit,
)

unit_registry = UnitRegistry()

# Temperature
temperature = PhysicalQuantity(
    name="Temperature",
    description="Temperature is a physical quantity that quantitatively expresses "
    "the attribute of hotness or coldness.",
    SIUnit=str(unit_registry.kelvin),
    SIUnitSymbol=f"{unit_registry.kelvin:~}",
)

kelvin = PhysicalUnit(
    name=str(unit_registry.kelvin),
    description="The Kelvin scale is an absolute scale, which is defined such that 0 K is absolute zero.",
    symbol=f"{unit_registry.kelvin:~}",
    physicalQuantity=temperature,
)

celsius = PhysicalUnit(
    name=str(unit_registry.celsius),
    description="The Celsius scale is based on 0°C for the freezing point of water "
    "and 100°C for the boiling point of water at 1 atm pressure.",
    symbol=f"{unit_registry.celsius:~}",
    physicalQuantity=temperature,
)

fahrenheit = PhysicalUnit(
    name=str(unit_registry.fahrenheit),
    description="The Fahrenheit scale where the freezing point of water is 32°F "
    "and the boiling point is 212°F at standard atmospheric pressure.",
    symbol=f"{unit_registry.fahrenheit:~}",
    physicalQuantity=temperature,
)

# Rotational Frequency
rotational_frequency = PhysicalQuantity(
    name="Rotational Frequency",
    description="Rotational frequency is the frequency of rotation of an object around an axis.",
    SIUnit=str(unit_registry.rps),
    SIUnitSymbol=f"{unit_registry.rps:~}",
)

rpm = PhysicalUnit(
    name=str(unit_registry.rpm),
    description="Revolutions per minute (rpm) is a unit of rotational speed or rotational frequency.",
    symbol=f"{unit_registry.rpm:~}",
    physicalQuantity=rotational_frequency,
)

rps = PhysicalUnit(
    name=str(unit_registry.rps),
    description="Revolutions per second (rps) is the SI unit of rotational frequency.",
    symbol=f"{unit_registry.rps:~}",
    physicalQuantity=rotational_frequency,
)

hertz = PhysicalUnit(
    name=str(unit_registry.hertz),
    description="Hertz (Hz) is the SI unit of frequency, defined as one cycle per second.",
    symbol=f"{unit_registry.hertz:~}",
    physicalQuantity=rotational_frequency,
)

# Pressure
pressure = PhysicalQuantity(
    name="Pressure",
    description="Pressure is the force applied perpendicular to the surface of an object per unit area.",
    SIUnit=str(unit_registry.pascal),
    SIUnitSymbol=f"{unit_registry.pascal:~}",
)

pascal = PhysicalUnit(
    name=str(unit_registry.pascal),
    description="The pascal (Pa) is the SI unit of pressure, defined as one newton per square meter.",
    symbol=f"{unit_registry.pascal:~}",
    physicalQuantity=pressure,
)

bar = PhysicalUnit(
    name=str(unit_registry.bar),
    description="The bar is a metric unit of pressure defined as exactly 100,000 pascals.",
    symbol=f"{unit_registry.bar:~}",
    physicalQuantity=pressure,
)

atmosphere = PhysicalUnit(
    name=str(unit_registry.atm),
    description="The standard atmosphere (atm) is a unit of pressure defined as 101,325 Pa.",
    symbol=f"{unit_registry.atm:~}",
    physicalQuantity=pressure,
)

psi = PhysicalUnit(
    name=str(unit_registry.psi),
    description="Pounds per square inch (psi) is a unit of pressure based on avoirdupois units.",
    symbol=f"{unit_registry.psi:~}",
    physicalQuantity=pressure,
)

torr = PhysicalUnit(
    name=str(unit_registry.torr),
    description="The torr is a unit of pressure based on an absolute scale, defined as 1/760 of a standard atmosphere.",
    symbol=f"{unit_registry.torr:~}",
    physicalQuantity=pressure,
)

# Speed
speed = PhysicalQuantity(
    name="Speed",
    description="Speed is the magnitude of velocity, measuring the rate of change of position with respect to time.",
    SIUnit=str(unit_registry("m/s").units),
    SIUnitSymbol=f"{unit_registry('m/s').units:~}",
)

meters_per_second = PhysicalUnit(
    name=str(unit_registry("m/s")),
    description="Meters per second (m/s) is the SI unit of speed.",
    symbol=f"{unit_registry('m/s'):~}",
    physicalQuantity=speed,
)

kilometers_per_hour = PhysicalUnit(
    name=str(unit_registry("km/h")),
    description="Kilometers per hour (km/h) is a unit of speed expressing "
    "the number of kilometers traveled in one hour.",
    symbol=f"{unit_registry('km/h'):~}",
    physicalQuantity=speed,
)

knots = PhysicalUnit(
    name=str(unit_registry.knot),
    description="The knot is a unit of speed equal to one nautical mile per hour, exactly 1.852 km/h.",
    symbol=f"{unit_registry.knot:~}",
    physicalQuantity=speed,
)

miles_per_hour = PhysicalUnit(
    name=str(unit_registry("mile/hour")),
    description="Miles per hour (mph) is a unit of speed expressing the number of statute miles covered in one hour.",
    symbol=f"{unit_registry('mile/hour'):~}",
    physicalQuantity=speed,
)

# Percentage
percentage = PhysicalQuantity(
    name="Percentage",
    description="A percentage is a number or ratio expressed as a fraction of 100.",
    SIUnit=str(unit_registry.percent),
    SIUnitSymbol=f"{unit_registry.percent:~}",
)

percent = PhysicalUnit(
    name=str(unit_registry.percent),
    description="Percent (%) represents a ratio as a fraction of 100.",
    symbol=f"{unit_registry.percent:~}",
    physicalQuantity=percentage,
)

# Angle
angle = PhysicalQuantity(
    name="Angle",
    description="An angle is the figure formed by two rays sharing a common endpoint.",
    SIUnit=str(unit_registry.radian),
    SIUnitSymbol=f"{unit_registry.radian:~}",
)

degree = PhysicalUnit(
    name=str(unit_registry.degree),
    description="A degree (°) is a measurement of plane angle, representing 1/360 of a full rotation.",
    symbol=f"{unit_registry.degree:~}",
    physicalQuantity=angle,
)

radian = PhysicalUnit(
    name=str(unit_registry.radian),
    description="A radian is the SI unit of angular measure, defined by the angle "
    "subtended at the center of a circle by an arc equal in length to the radius.",
    symbol=f"{unit_registry.radian:~}",
    physicalQuantity=angle,
)

# Length
length = PhysicalQuantity(
    name="Length",
    description="Length is a measure of distance.",
    SIUnit=str(unit_registry.meter),
    SIUnitSymbol=f"{unit_registry.meter:~}",
)

meter = PhysicalUnit(
    name=str(unit_registry.meter),
    description="The meter is the SI base unit of length.",
    symbol=f"{unit_registry.meter:~}",
    physicalQuantity=length,
)

kilometer = PhysicalUnit(
    name=str(unit_registry.kilometer),
    description="A kilometer is a unit of length equal to 1000 meters.",
    symbol=f"{unit_registry.kilometer:~}",
    physicalQuantity=length,
)

mile = PhysicalUnit(
    name=str(unit_registry.mile),
    description="A mile is a unit of length equal to 1.60934 kilometers or 5280 feet.",
    symbol=f"{unit_registry.mile:~}",
    physicalQuantity=length,
)

foot = PhysicalUnit(
    name=str(unit_registry.foot),
    description="A foot is a unit of length equal to 0.3048 meters.",
    symbol=f"{unit_registry.foot:~}",
    physicalQuantity=length,
)

inch = PhysicalUnit(
    name=str(unit_registry.inch),
    description="An inch is a unit of length equal to exactly 2.54 centimeters.",
    symbol=f"{unit_registry.inch:~}",
    physicalQuantity=length,
)

nautical_mile = PhysicalUnit(
    name=str(unit_registry.nautical_mile),
    description="A nautical mile is a unit of length used in marine and air navigation, equal to exactly 1,852 meters.",
    symbol=f"{unit_registry.nautical_mile:~}",
    physicalQuantity=length,
)

# Power
power = PhysicalQuantity(
    name="Power",
    description="Power is the rate at which energy is transferred, used, or transformed.",
    SIUnit=str(unit_registry.watt),
    SIUnitSymbol=f"{unit_registry.watt:~}",
)

watt = PhysicalUnit(
    name=str(unit_registry.watt),
    description="The watt is the SI unit of power, defined as one joule per second.",
    symbol=f"{unit_registry.watt:~}",
    physicalQuantity=power,
)

kilowatt = PhysicalUnit(
    name=str(unit_registry.kilowatt),
    description="A kilowatt is a unit of power equal to one thousand watts.",
    symbol=f"{unit_registry.kilowatt:~}",
    physicalQuantity=power,
)

horsepower = PhysicalUnit(
    name=str(unit_registry.horsepower),
    description="Horsepower is a unit of power, with one mechanical horsepower equal to about 745.7 watts.",
    symbol=f"{unit_registry.horsepower:~}",
    physicalQuantity=power,
)

megawatt = PhysicalUnit(
    name=str(unit_registry.megawatt),
    description="A megawatt is a unit of power equal to one million watts.",
    symbol=f"{unit_registry.megawatt:~}",
    physicalQuantity=power,
)

# Volumetric Flow Rate
volumetric_flow_rate = PhysicalQuantity(
    name="Volumetric Flow Rate",
    description="Volumetric flow rate is the volume of fluid which passes through a given surface per unit time.",
    SIUnit=str(unit_registry.meter**3 / unit_registry.second),
    SIUnitSymbol=f"{unit_registry.meter**3 / unit_registry.second:~}",
)

cubic_meter_per_second = PhysicalUnit(
    name=str(unit_registry.meter**3 / unit_registry.second),
    description="The cubic meter per second is the SI unit of volumetric flow rate.",
    symbol=f"{unit_registry.meter**3 / unit_registry.second:~}",
    physicalQuantity=volumetric_flow_rate,
)

liter_per_hour = PhysicalUnit(
    name=str(unit_registry.liter / unit_registry.hour),
    description="A liter per hour measures the volume of fluid that passes through a given surface in one hour.",
    symbol=f"{unit_registry.liter / unit_registry.hour:~}",
    physicalQuantity=volumetric_flow_rate,
)

gallons_per_minute = PhysicalUnit(
    name=str(unit_registry.gallon / unit_registry.minute),
    description="Gallons per minute (GPM) is a measure of the volume flow rate of a liquid.",
    symbol=f"{unit_registry.gallon / unit_registry.minute:~}",
    physicalQuantity=volumetric_flow_rate,
)

cubic_feet_per_minute = PhysicalUnit(
    name=str(unit_registry.cubic_foot / unit_registry.minute),
    description="Cubic feet per minute (CFM) is a measure of volumetric flow rate.",
    symbol=f"{unit_registry.cubic_foot / unit_registry.minute:~}",
    physicalQuantity=volumetric_flow_rate,
)

# Mass
mass = PhysicalQuantity(
    name="Mass",
    description="Mass is a property of a physical body and a measure "
    "of its resistance to acceleration when a net force is applied.",
    SIUnit=str(unit_registry.kilogram),
    SIUnitSymbol=f"{unit_registry.kilogram:~}",
)

kilogram = PhysicalUnit(
    name=str(unit_registry.kilogram),
    description="The kilogram is the SI base unit of mass, defined by the Planck constant.",
    symbol=f"{unit_registry.kilogram:~}",
    physicalQuantity=mass,
)

gram = PhysicalUnit(
    name=str(unit_registry.gram),
    description="A gram is a metric unit of mass equal to one thousandth of a kilogram.",
    symbol=f"{unit_registry.gram:~}",
    physicalQuantity=mass,
)

metric_ton = PhysicalUnit(
    name=str(unit_registry.metric_ton),
    description="A metric ton (tonne) is a unit of mass equal to 1000 kilograms.",
    symbol=f"{unit_registry.metric_ton:~}",
    physicalQuantity=mass,
)

pound = PhysicalUnit(
    name=str(unit_registry.pound),
    description="The pound is a unit of mass used in the imperial system, defined exactly as 0.45359237 kilograms.",
    symbol=f"{unit_registry.pound:~}",
    physicalQuantity=mass,
)

ounce = PhysicalUnit(
    name=str(unit_registry.ounce),
    description="An ounce is a unit of mass equal to approximately 28.35 grams or 1/16 of a pound.",
    symbol=f"{unit_registry.ounce:~}",
    physicalQuantity=mass,
)

# Energy
energy = PhysicalQuantity(
    name="Energy",
    description="Energy is the capacity for doing work. It may exist in "
    "potential, kinetic, thermal, electrical, chemical, nuclear, or other various forms.",
    SIUnit=str(unit_registry.joule),
    SIUnitSymbol=f"{unit_registry.joule:~}",
)

joule = PhysicalUnit(
    name=str(unit_registry.joule),
    description="The joule is the SI unit of energy, equal to the energy transferred "
    "when applying a force of one newton through a distance of one meter.",
    symbol=f"{unit_registry.joule:~}",
    physicalQuantity=energy,
)

kilowatt_hour = PhysicalUnit(
    name=str(unit_registry.kilowatt_hour),
    description="A kilowatt-hour is a unit of energy equal to 3.6 megajoules.",
    symbol=f"{unit_registry.kilowatt_hour:~}",
    physicalQuantity=energy,
)

calorie = PhysicalUnit(
    name=str(unit_registry.calorie),
    description="A calorie is a unit of energy equal to about 4.184 joules.",
    symbol=f"{unit_registry.calorie:~}",
    physicalQuantity=energy,
)

electron_volt = PhysicalUnit(
    name=str(unit_registry.electron_volt),
    description="The electron volt is a unit of energy equal to approximately 1.602×10^−19 joules.",
    symbol=f"{unit_registry.electron_volt:~}",
    physicalQuantity=energy,
)

# Time
time = PhysicalQuantity(
    name="Time",
    description="Time is the indefinite continued progress of existence and events that occur in an apparently "
    "irreversible succession from the past, through the present, into the future.",
    SIUnit=str(unit_registry.second),
    SIUnitSymbol=f"{unit_registry.second:~}",
)

second = PhysicalUnit(
    name=str(unit_registry.second),
    description="The second is the SI base unit of time, defined by taking"
    " the fixed numerical value of the caesium frequency.",
    symbol=f"{unit_registry.second:~}",
    physicalQuantity=time,
)

minute = PhysicalUnit(
    name=str(unit_registry.minute),
    description="A minute is a unit of time equal to 60 seconds.",
    symbol=f"{unit_registry.minute:~}",
    physicalQuantity=time,
)

hour = PhysicalUnit(
    name=str(unit_registry.hour),
    description="An hour is a unit of time equal to 60 minutes or 3600 seconds.",
    symbol=f"{unit_registry.hour:~}",
    physicalQuantity=time,
)

day = PhysicalUnit(
    name=str(unit_registry.day),
    description="A day is a unit of time equal to 24 hours or 86,400 seconds.",
    symbol=f"{unit_registry.day:~}",
    physicalQuantity=time,
)

week = PhysicalUnit(
    name=str(unit_registry.week),
    description="A week is a unit of time equal to 7 days.",
    symbol=f"{unit_registry.week:~}",
    physicalQuantity=time,
)

year = PhysicalUnit(
    name=str(unit_registry.year),
    description="A year is approximately the time it takes for the Earth to complete one revolution around the Sun.",
    symbol=f"{unit_registry.year:~}",
    physicalQuantity=time,
)

# Force
force = PhysicalQuantity(
    name="Force",
    description="Force is any interaction that, when unopposed, will change the motion of an object.",
    SIUnit=str(unit_registry.newton),
    SIUnitSymbol=f"{unit_registry.newton:~}",
)

newton = PhysicalUnit(
    name=str(unit_registry.newton),
    description="The newton is the SI unit of force. It is defined as the force required "
    "to accelerate a mass of one kilogram at a rate of one meter per second squared.",
    symbol=f"{unit_registry.newton:~}",
    physicalQuantity=force,
)

pound_force = PhysicalUnit(
    name=str(unit_registry.pound_force),
    description="The pound-force is a unit of force in some systems of measurement "
    "including English Engineering units and British Gravitational units.",
    symbol=f"{unit_registry.pound_force:~}",
    physicalQuantity=force,
)

dyne = PhysicalUnit(
    name=str(unit_registry.dyne),
    description="The dyne is a unit of force in the CGS system, equal to 10^-5 newtons.",
    symbol=f"{unit_registry.dyne:~}",
    physicalQuantity=force,
)

# Area
area = PhysicalQuantity(
    name="Area",
    description="Area is the quantity that expresses the extent of a two-dimensional figure or shape in the plane.",
    SIUnit=str(unit_registry.meter**2),
    SIUnitSymbol=f"{unit_registry.meter**2:~}",
)

square_meter = PhysicalUnit(
    name=str(unit_registry.meter**2),
    description="The square meter is the SI unit of area.",
    symbol=f"{unit_registry.meter**2:~}",
    physicalQuantity=area,
)

square_kilometer = PhysicalUnit(
    name=str(unit_registry.kilometer**2),
    description="The square kilometer is a unit of area equal to 1,000,000 square meters.",
    symbol=f"{unit_registry.kilometer**2:~}",
    physicalQuantity=area,
)

hectare = PhysicalUnit(
    name=str(unit_registry.hectare),
    description="The hectare is a non-SI metric unit of area equal to 10,000 square meters or one square hectometer.",
    symbol=f"{unit_registry.hectare:~}",
    physicalQuantity=area,
)

acre = PhysicalUnit(
    name=str(unit_registry.acre),
    description="The acre is a unit of land area used in the imperial and US customary systems.",
    symbol=f"{unit_registry.acre:~}",
    physicalQuantity=area,
)

# Volume
volume = PhysicalQuantity(
    name="Volume",
    description="Volume is the quantity of three-dimensional space enclosed by a closed surface.",
    SIUnit=str(unit_registry.meter**3),
    SIUnitSymbol=f"{unit_registry.meter**3:~}",
)

cubic_meter = PhysicalUnit(
    name=str(unit_registry.meter**3),
    description="The cubic meter is the SI unit of volume.",
    symbol=f"{unit_registry.meter**3:~}",
    physicalQuantity=volume,
)

liter = PhysicalUnit(
    name=str(unit_registry.liter),
    description="The liter is a metric unit of volume equal to 1 cubic decimeter.",
    symbol=f"{unit_registry.liter:~}",
    physicalQuantity=volume,
)

gallon = PhysicalUnit(
    name=str(unit_registry.gallon),
    description="The gallon is a unit of volume in imperial and US customary systems.",
    symbol=f"{unit_registry.gallon:~}",
    physicalQuantity=volume,
)

cubic_foot = PhysicalUnit(
    name=str(unit_registry.cubic_foot),
    description="The cubic foot is an imperial and US customary unit of volume.",
    symbol=f"{unit_registry.cubic_foot:~}",
    physicalQuantity=volume,
)

# Density
density = PhysicalQuantity(
    name="Density",
    description="Density is the mass per unit volume of a substance.",
    SIUnit=str(unit_registry.kilogram / unit_registry.meter**3),
    SIUnitSymbol=f"{unit_registry.kilogram / unit_registry.meter**3:~}",
)

kilogram_per_cubic_meter = PhysicalUnit(
    name=str(unit_registry.kilogram / unit_registry.meter**3),
    description="Kilogram per cubic meter is the SI unit of density.",
    symbol=f"{unit_registry.kilogram / unit_registry.meter**3:~}",
    physicalQuantity=density,
)

gram_per_cubic_centimeter = PhysicalUnit(
    name=str(unit_registry.gram / unit_registry.centimeter**3),
    description="Gram per cubic centimeter is a common unit of density.",
    symbol=f"{unit_registry.gram / unit_registry.centimeter**3:~}",
    physicalQuantity=density,
)

# Electric Current
electric_current = PhysicalQuantity(
    name="Electric Current",
    description="Electric current is the rate of flow of electric charge past a point or region.",
    SIUnit=str(unit_registry.ampere),
    SIUnitSymbol=f"{unit_registry.ampere:~}",
)

ampere = PhysicalUnit(
    name=str(unit_registry.ampere),
    description="The ampere is the SI base unit of electric current.",
    symbol=f"{unit_registry.ampere:~}",
    physicalQuantity=electric_current,
)

# Voltage
voltage = PhysicalQuantity(
    name="Voltage",
    description="Voltage, also called electromotive force, is the difference in electric potential between two points.",
    SIUnit=str(unit_registry.volt),
    SIUnitSymbol=f"{unit_registry.volt:~}",
)

volt = PhysicalUnit(
    name=str(unit_registry.volt),
    description="The volt is the SI derived unit for electric potential, "
    "electric potential difference, and electromotive force.",
    symbol=f"{unit_registry.volt:~}",
    physicalQuantity=voltage,
)

# Resistance
resistance = PhysicalQuantity(
    name="Resistance",
    description="Electrical resistance is the opposition to the flow of electric current through a material.",
    SIUnit=str(unit_registry.ohm),
    SIUnitSymbol=f"{unit_registry.ohm:~}",
)

ohm = PhysicalUnit(
    name=str(unit_registry.ohm),
    description="The ohm is the SI derived unit of electrical resistance.",
    symbol=f"{unit_registry.ohm:~}",
    physicalQuantity=resistance,
)

# Frequency
frequency = PhysicalQuantity(
    name="Frequency",
    description="Frequency is the number of occurrences of a repeating event per unit of time.",
    SIUnit=str(unit_registry.hertz),
    SIUnitSymbol=f"{unit_registry.hertz:~}",
)

hertz = PhysicalUnit(
    name=str(unit_registry.hertz),
    description="The hertz is the derived unit of frequency in the SI.",
    symbol=f"{unit_registry.hertz:~}",
    physicalQuantity=frequency,
)

# Luminous Intensity
luminous_intensity = PhysicalQuantity(
    name="Luminous Intensity",
    description="Luminous intensity is the quantity of visible light emitted by a source per unit solid angle.",
    SIUnit=str(unit_registry.candela),
    SIUnitSymbol=f"{unit_registry.candela:~}",
)

candela = PhysicalUnit(
    name=str(unit_registry.candela),
    description="The candela is the SI base unit of luminous intensity.",
    symbol=f"{unit_registry.candela:~}",
    physicalQuantity=luminous_intensity,
)

# This list can be further extended with more quantities and units as needed.
