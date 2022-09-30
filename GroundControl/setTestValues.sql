/****** Script for SelectTopNRows command from SSMS  ******/
UPDATE [dtr].[dbo].[maneuverToExecute] SET requestedState = 'manualTesting',
	manual_up = 0,
	manual_throttle = 0,
	manual_yaw = 0,
	manual_servo = 0,
	scalar_up = 0,
	scalar_yaw = 0,
	scalar_throttle = 0,
	p_throttle = 0.1,
	i_throttle = 0.2,
	d_throttle = 0.3,
	p_yaw = 0.4,
	i_yaw = 0.5,
	d_yaw = 0.6
	

SELECT * FROM [dtr].[dbo].[maneuverToExecute]