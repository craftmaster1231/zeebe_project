CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE Core
(
    BuildingName        VARCHAR(255),
    DesignPowerCapacity DECIMAL(10, 2),
    DeviceName          VARCHAR(255),
    DeviceType          VARCHAR(255),
    Id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    Manufacturer        VARCHAR(255),
    Model               VARCHAR(255)
);

CREATE TABLE Placement
(
    SpaceName   VARCHAR(255),
    SpaceId     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ParentId    UUID REFERENCES Core (Id),
    Type        VARCHAR(255),
    XCoordinate DECIMAL(10, 2),
    YCoordinate DECIMAL(10, 2),
    ZCoordinate DECIMAL(10, 2),
    Rotation    DECIMAL(10, 2),
    RackSide    VARCHAR(10),
    RU          INT,
    Location    INT,
    UHeight     INT,
    XOffset     DECIMAL(10, 2),
    XPosition   DECIMAL(10, 2)
);

CREATE TYPE ConnectionTypeEnum AS ENUM ('POWER_CONNECTION', 'DATA_CONNECTION');

CREATE TABLE Device_Connections
(
    ConnectionFromDevice UUID REFERENCES Core (Id),
    ConnectedFromPort    VARCHAR(255),
    ConnectedToDevice    UUID REFERENCES Core (Id),
    ConnectedToPort      VARCHAR(255),
    ConnectionType       ConnectionTypeEnum
);

INSERT INTO Core (BuildingName, DesignPowerCapacity, DeviceName, DeviceType, Id, Manufacturer, Model)
VALUES ('Building A', 150.50, 'Device 1', 'Sensor', '550e8400-e29b-41d4-a716-446655440000', 'ABC Inc.', 'Model X'),
       ('Building B', 200.75, 'Device 2', 'Camera', '123e4567-e89b-12d3-a456-426614174001', 'XYZ Corp.', 'Model Y');

INSERT INTO Placement (SpaceName, ParentId, Type, XCoordinate, YCoordinate, ZCoordinate, Rotation, RackSide, RU,
                       Location, UHeight, XOffset, XPosition)
VALUES ('Space 1', NULL, 'Type A', 10.5, 20.3, 15.7, 90.0, 'Left', 1, 101, 2, 5.5, 10.0),
       ('Space 2', '550e8400-e29b-41d4-a716-446655440000', 'Type B', 15.0, 25.3, 12.0, 45.0, 'Right', 2, 102, 4, 7.5,
        15.0);

INSERT INTO Device_Connections (ConnectionFromDevice, ConnectedFromPort, ConnectedToDevice, ConnectedToPort,
                                ConnectionType)
VALUES ('550e8400-e29b-41d4-a716-446655440000', 'Port1', '123e4567-e89b-12d3-a456-426614174001', 'Port2',
        'POWER_CONNECTION');
