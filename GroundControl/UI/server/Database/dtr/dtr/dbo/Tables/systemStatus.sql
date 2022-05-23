CREATE TABLE [dbo].[systemStatus] (
    [ID]                 INT           IDENTITY (1, 1) NOT NULL,
    [blimpLastHeartbeat] DATETIME      NULL,
    [cameraDetectionStr] VARCHAR (MAX) NULL,
    PRIMARY KEY CLUSTERED ([ID] ASC)
);

