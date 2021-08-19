import logging

import haversine as hs

logger = logging.getLogger(__file__)

class AppException(BaseException):
    pass

class ValidationError(AppException):
    pass

class SpeedValidationError(ValidationError):
    pass

class DisplacementSpeedValidationError(ValidationError):
    pass

class AltitudeValidationError(ValidationError):
    pass

class DriverNotMovingError(ValidationError):
    pass


def prepare_position(position, last_driver_position, settings):
    position.displacement_speed = calculate_displacement_speed(position, last_driver_position)
    try:
        position.is_valid = validate_position(position, last_driver_position, settings)
    except ValidationError as e:
        position.is_valid = False
        logger.warning(e)
    return position


def calculate_displacement_speed(position, last_driver_position):
    if not last_driver_position:
        return None
    displacement = hs.haversine((position.latitude, position.longitude),
                                (last_driver_position.latitude, last_driver_position.longitude))
    time = position.received_at - last_driver_position.received_at
    displacement_speed = displacement / time.seconds * 3600
    return displacement_speed


def validate_position(position, last_driver_position, settings):
    if position.speed > settings.MAX_SPEED:
        raise SpeedValidationError(f'Driver: {position.driver_id} has higher speed({position.speed}) than max allowed({settings.MAX_SPEED})')
    if position.altitude > settings.MAX_ALTITUDE:
        raise AltitudeValidationError(f'Driver: {position.driver_id} has higher altutude({position.altitude}) than max allowed({settings.MAX_ALTITUDE})')
    if last_driver_position and position.displacement_speed == 0 and position.speed != 0:
        # Car stay on the same place
        raise DisplacementSpeedValidationError(f'Driver: {position.driver_id} is not moving, but speed is not 0')
    if position.displacement_speed > settings.MAX_SPEED:
        raise DisplacementSpeedValidationError(
            f'Driver: {position.driver_id} moved from coordinates{(last_driver_position.latitude, last_driver_position.longitude)}'
            f' to {(position.latitude, position.longitude)} with higher speed({position.displacement_speed}) than allowed({settings.MAX_SPEED})'
        )
    return True


def validate(position, last_driver_position, settings):
    if position.speed > settings.MAX_SPEED:
        position.is_valid = False
        logger.warning(
            f'Driver: {position.driver_id} has higher speed({position.speed}) than max allowed({settings.MAX_SPEED})')
        return position
    if position.altitude > settings.MAX_ALTITUDE:
        position.is_valid = False
        logger.warning(
            f'Driver: {position.driver_id} has higher altutude({position.altitude}) than max allowed({settings.MAX_ALTITUDE})')
        return position
    if not last_driver_position:
        return position
    displacement = hs.haversine((position.latitude, position.longitude),
                                (last_driver_position.latitude, last_driver_position.longitude))
    if displacement == 0 and position.speed != 0:
        # Car stay on the same place
        position.is_valid = False
        logger.warning(f'Driver: {position.driver_id} is not moving, but speed is not 0')
        return position
    time = position.received_at - last_driver_position.received_at
    calculated_speed = displacement / time.seconds * 3600
    if calculated_speed > settings.MAX_SPEED:
        position.is_valid = False
        logger.warning(
            f'Driver: {position.driver_id} moved from coordinates{(last_driver_position.latitude, last_driver_position.longitude)}'
            f' to {(position.latitude, position.longitude)}, time({time}), displacement({displacement}) with speed({calculated_speed}), allowed spped({settings.MAX_SPEED})')
        return position
    position.is_valid = True
    position.calculated_speed = calculated_speed
    return position
