USE [master]
GO
/****** Object:  Database [dtr]    Script Date: 11/10/2022 8:43:06 AM ******/
CREATE DATABASE [dtr]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'dtr', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\DATA\dtr.mdf' , SIZE = 598016KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'dtr_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\DATA\dtr_log.ldf' , SIZE = 1449984KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [dtr] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [dtr].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [dtr] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [dtr] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [dtr] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [dtr] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [dtr] SET ARITHABORT OFF 
GO
ALTER DATABASE [dtr] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [dtr] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [dtr] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [dtr] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [dtr] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [dtr] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [dtr] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [dtr] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [dtr] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [dtr] SET  DISABLE_BROKER 
GO
ALTER DATABASE [dtr] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [dtr] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [dtr] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [dtr] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [dtr] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [dtr] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [dtr] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [dtr] SET RECOVERY FULL 
GO
ALTER DATABASE [dtr] SET  MULTI_USER 
GO
ALTER DATABASE [dtr] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [dtr] SET DB_CHAINING OFF 
GO
ALTER DATABASE [dtr] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [dtr] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [dtr] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [dtr] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
EXEC sys.sp_db_vardecimal_storage_format N'dtr', N'ON'
GO
ALTER DATABASE [dtr] SET QUERY_STORE = OFF
GO
USE [dtr]
GO
/****** Object:  Table [dbo].[blimpCodeUploader]    Script Date: 11/10/2022 8:43:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[blimpCodeUploader](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[isUploadRequested] [bit] NULL,
	[uploaderStateID] [int] NULL,
	[lastRunTimeError] [varchar](max) NULL,
	[datetimeLastUpload] [datetime] NULL,
	[updateStatus] [varchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[blimpCodeUploadStates]    Script Date: 11/10/2022 8:43:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[blimpCodeUploadStates](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[uploadStates] [varchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[dataLogs]    Script Date: 11/10/2022 8:43:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[dataLogs](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[logTime] [datetime] NULL,
	[lidarDistance] [float] NULL,
	[irSensor] [int] NULL,
	[upMotor] [float] NULL,
	[throttleMotor] [float] NULL,
	[yawMotor] [float] NULL,
	[servoDoor] [int] NULL,
	[p_up] [float] NULL,
	[isMicroPython] [bit] NULL,
	[i_up] [float] NULL,
	[d_up] [float] NULL,
	[p_throttle] [float] NULL,
	[i_throttle] [float] NULL,
	[d_throttle] [float] NULL,
	[p_yaw] [float] NULL,
	[i_yaw] [float] NULL,
	[d_yaw] [float] NULL,
	[scalar_up] [float] NULL,
	[scalar_yaw] [float] NULL,
	[scalar_throttle] [float] NULL,
	[error_rounding_up] [float] NULL,
	[error_scaling_up] [float] NULL,
	[pid_min_up] [float] NULL,
	[controlAuthority] [varchar](max) NULL,
	[loopTime] [float] NULL,
	[currentManeuver] [varchar](max) NULL,
	[state_description] [varchar](max) NULL,
	[state_target] [varchar](max) NULL,
	[state_action] [varchar](max) NULL,
	[ballIsFound] [bit] NULL,
	[yellowGoalIsFound] [bit] NULL,
	[orangeGoalIsFound] [bit] NULL,
	[imu_yaw] [float] NULL,
	[imu_yaw_rate] [float] NULL,
	[imu_yaw_limited] [float] NULL,
	[imu_yaw_rate_limited] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[errorLogs]    Script Date: 11/10/2022 8:43:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[errorLogs](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[errorTime] [datetime] NULL,
	[error] [varchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[loggerPrints]    Script Date: 11/10/2022 8:43:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[loggerPrints](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[logLines] [varchar](max) NULL,
	[logTime] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[maneuverToExecute]    Script Date: 11/10/2022 8:43:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[maneuverToExecute](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[baseUpVal] [float] NULL,
	[duration] [float] NULL,
	[firstManeuver] [varchar](max) NULL,
	[secondManeuver] [varchar](max) NULL,
	[mockSensor_greenDetected] [varchar](max) NULL,
	[mockSensor_aprilTagDetected] [varchar](max) NULL,
	[p_up] [float] NULL,
	[i_up] [float] NULL,
	[d_up] [float] NULL,
	[p_throttle] [float] NULL,
	[i_throttle] [float] NULL,
	[d_throttle] [float] NULL,
	[p_yaw] [float] NULL,
	[i_yaw] [float] NULL,
	[d_yaw] [float] NULL,
	[scalar_up] [float] NULL,
	[scalar_yaw] [float] NULL,
	[scalar_throttle] [float] NULL,
	[requestedState] [varchar](max) NULL,
	[manual_up] [float] NULL,
	[manual_throttle] [float] NULL,
	[manual_yaw] [float] NULL,
	[manual_servo] [float] NULL,
	[pid_upSetValue] [float] NULL,
	[control] [varchar](max) NULL,
	[manualHeight] [float] NULL,
	[resetOpenMVforFTPtsfr] [bit] NULL,
	[pid_min_up] [float] NULL,
	[error_scaling_up] [float] NULL,
	[error_rounding_up] [float] NULL,
	[doFtpLoadAndReset] [bit] NULL,
	[yawRate] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[static_systemStates]    Script Date: 11/10/2022 8:43:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[static_systemStates](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[state] [varchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[systemStatus]    Script Date: 11/10/2022 8:43:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[systemStatus](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[blimpLastHeartbeat] [datetime] NULL,
	[cameraDetectionStr] [varchar](max) NULL,
	[isIrSensorDetection] [bit] NULL,
	[currentManeuver] [varchar](max) NULL,
	[state_description] [varchar](max) NULL,
	[state_target] [varchar](max) NULL,
	[state_action] [varchar](max) NULL,
	[lidarDistance] [float] NULL,
	[upMotor] [float] NULL,
	[throttleMotor] [float] NULL,
	[yawMotor] [float] NULL,
	[servoDoor] [int] NULL,
	[controlAuthority] [varchar](max) NULL,
	[ballIsFound] [bit] NULL,
	[yellowGoalIsFound] [bit] NULL,
	[orangeGoalIsFound] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
USE [master]
GO
ALTER DATABASE [dtr] SET  READ_WRITE 
GO
