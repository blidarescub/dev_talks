using System;
using System.Device.Location;
using Windows.Devices.Geolocation;

namespace SmartBike
{
    public static class CoordinateConverter
    {
        public static GeoCoordinate ConvertGeocoordinate(Geocoordinate geocoordinate)
        {
            return new GeoCoordinate
                (
                geocoordinate.Point.Position.Latitude,
                geocoordinate.Point.Position.Longitude,
                geocoordinate.Point.Position.Altitude,
                geocoordinate.Accuracy,
                geocoordinate.AltitudeAccuracy ?? double.NaN,
                geocoordinate.Speed ?? double.NaN,
                geocoordinate.Heading ?? double.NaN
                );
        }
    }
}
