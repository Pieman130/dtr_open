close all
plot(plotHoverDataFriAm.logTime,plotHoverDataFriAm.lidarDistance)
hold on;
plot(plotHoverDataFriAm.logTime,ones(1,length(plotHoverDataFriAm.logTime))*550,'r') 

ylabel('distance from ceiling (cm)')

yyaxis right;
plot(plotHoverDataFriAm.logTime,plotHoverDataFriAm.upMotor)
plot(plotHoverDataFriAm.logTime,plotHoverDataFriAm.loopTime,'g') 
legend('lidar data','set point','motor val','loopTime')
xlabel('time')
ylabel('motor val/loop time')
