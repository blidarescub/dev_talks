using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Device.Location;
using System.Net;
using Windows.Web.Http;
using System.Runtime.Serialization.Json;
using System.Windows;
using Windows.Data.Json;
using System.Windows.Threading;

namespace SmartBike.Models
{
    class ServiceController
    {
        private const string URL = "http://52.32.72.73:8000";

        private List<Bike> m_bikeList;
        private Bike m_bike;

        public List<Bike> BikeList
        {
            get
            {
                return m_bikeList;
            }

            set
            {
                m_bikeList = value;
            }
        }

        internal Bike Bike
        {
            get
            {
                return m_bike;
            }

            set
            {
                m_bike = value;
            }
        }

        public async Task GetBikes(GeoCoordinate location)
        {
            BikeList = new List<Bike>();

            try
            {
                using(var client = new HttpClient())
                { 
                    var uri = new Uri(string.Format("{0}/bikes/?latitude={1}&longitude={2}", URL, location.Latitude, location.Longitude));
                    var response = await client.GetAsync(uri);
                    response.EnsureSuccessStatusCode();

                    var responseStream = await response.Content.ReadAsStringAsync();
                    var responseJson = JsonObject.Parse(responseStream);

                    if(!responseJson["success"].GetBoolean())
                    {
                        throw new BikeListLoadException("Could not load the list of Bikes from the server.");
                    }

                    foreach(var bikeJson in responseJson["bikes"].GetArray())
                    {
                        var jsonObject = bikeJson.GetObject();
                        BikeList.Add(new Bike((int)jsonObject["id"].GetNumber(), new GeoCoordinate(jsonObject["latitude"].GetNumber(), jsonObject["longitude"].GetNumber())));
                    }
                }
            }
            catch(Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        public async Task ReserveBike()
        {
            try
            {
                using(var client = new HttpClient())
                {
                    var uri = new Uri(string.Format("{0}/bike/?bike_id={1}&action=reserve", URL, Bike.Id.ToString()));
                    var response = await client.GetAsync(uri);
                    response.EnsureSuccessStatusCode();

                    var responseStream = await response.Content.ReadAsStringAsync();
                    var responseJson = JsonObject.Parse(responseStream);

                    if (!responseJson["success"].GetBoolean())
                    {
                        throw new BikeReserveException("Could not reserve the Bike.");
                    }

                    MessageBox.Show("The bike is yours! :) For now ...", "SUCCESS", MessageBoxButton.OK);
                }
            }
            catch(Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        public async Task FreeBike()
        {
            try
            {
                using (var client = new HttpClient())
                {
                    var uri = new Uri(string.Format("{0}/bike/?bike_id={1}&action=free", URL, Bike.Id.ToString()));
                    var response = await client.GetAsync(uri);
                    response.EnsureSuccessStatusCode();

                    var responseStream = await response.Content.ReadAsStringAsync();
                    var responseJson = JsonObject.Parse(responseStream);

                    if (!responseJson["success"].GetBoolean())
                    {
                        throw new BikeReserveException("Could not reserve the Bike.");
                    }

                    MessageBox.Show("Bike has been set free :D", "SUCCESS", MessageBoxButton.OK);
                    Bike = null;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

    }

    class BikeListLoadException : Exception
    {
        public BikeListLoadException(string message) { }
    }

    class BikeReserveException : Exception
    {
        public BikeReserveException(string message) { }
    }
}
