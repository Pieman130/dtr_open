SELECT ID, logTime,lidarDistance,upMotor,controlAuthority,currentManeuver,state_description,state_target,state_action,loopTime,  cast(logTime - LAG(logTime) OVER (ORDER BY logTime) as FLOAT) AS days_since_last_case
	 --logTime,yawMotor,p_yaw,i_yaw,d_yaw,scalar_yaw,loopTime,controlAuthority,currentManeuver, state_description,state_target,state_action,imu_yaw,imu_yaw_rate,imu_yaw_limited,imu_yaw_rate_limited,loopTime
  FROM [dtr].[dbo].[dataLogs]
  WHERE logTime >= '2022-11-11 09:39' and logTime <= '2022-11-11 09:43' and controlAuthority = 'auto' -- and loopTime> 0.4
