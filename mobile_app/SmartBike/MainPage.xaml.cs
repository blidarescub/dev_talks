using System;
using System.Linq;
using System.Windows;
using Microsoft.Phone.Shell;
using Microsoft.Phone.Controls;
using SmartBike.Resources;
using Microsoft.Phone.Maps;
using Microsoft.Phone.Maps.Controls;
using System.Device.Location;
using Windows.Devices.Geolocation;
using System.Windows.Shapes;
using System.Windows.Media;
using SmartBike.Models;
using System.Windows.Media.Imaging;
using System.Windows.Controls;
using System.Threading.Tasks;
using System.Windows.Input;

namespace SmartBike
{
    public partial class MainPage : PhoneApplicationPage
    {
        const int DEFAULT_ZOOM_LEVEL = 17;
        const int MIN_ZOOMLEVEL_FOR_LANDMARKS = 16;
        const string APPLICATION_ID = "SmartBike";
        const string APPLICATION_TOKEN = "AnU_3nQ-r2OUr73hSXmpPEU8Pwwp-FiqnhvmN74ZQyBtam_l7FW5PfUd-IiD-1tB";

        ToggleStatus landmarksToggleStatus = ToggleStatus.ToggledOff;

        GeoCoordinate currentLocation = null;
        MapLayer locationLayer = null;
        MapLayer bikeLayer = null;

        ServiceController svcController;

        public MainPage()
        {

            InitializeComponent();

            BuildLocalizedApplicationBar();

            bikeLayer = new MapLayer();
            locationLayer = new MapLayer();
            bikeMap.LandmarksEnabled = false;
            bikeMap.PedestrianFeaturesEnabled = false;
            bikeMap.CartographicMode = MapCartographicMode.Road;
            bikeMap.ColorMode = MapColorMode.Dark;
            bikeMap.Layers.Add(bikeLayer);
            bikeMap.Layers.Add(locationLayer);
            bikeMap.ZoomLevel = DEFAULT_ZOOM_LEVEL;

            svcController = new ServiceController();

            try
            {
                // hardcoding current location as GPS is not avaialble
                currentLocation = new GeoCoordinate(44.426934, 26.105354); // @ Biblioteca Nationala Bucuresti

                GetLocation();
                CenterMapOnLocation();
                ShowLocation();
                Task.Factory.StartNew(() => InitializeBikes());

            }
            catch (Exception ex)
            {
                MessageBox.Show(string.Format("ERROR: {0}\n{1}", ex.Message, ex.StackTrace));
            }

        }

        private async Task InitializeBikes()
        {
            await svcController.GetBikes(currentLocation);

            Dispatcher.BeginInvoke(() =>
            {
                foreach (var bike in svcController.BikeList)
                {
                    DrawBike(bike.Id, bike.Location);
                }
            });
        }

        private void bikeMap_Loaded(object sender, RoutedEventArgs e)
        {
            MapsSettings.ApplicationContext.ApplicationId = APPLICATION_ID;
            MapsSettings.ApplicationContext.AuthenticationToken = APPLICATION_TOKEN;
        }

        #region Event handlers for App Bar buttons and menu items

        void ToggleLocation(object sender, EventArgs e)
        {
            //SignupPage userControl = new SignupPage();
            //Application.LoadComponent(userControl, new Uri("/Views/SignupPage.xaml", UriKind.Relative));
            //CenterMapOnLocation();
        }

        void ToggleLandmarks(object sender, EventArgs e)
        {
            switch (landmarksToggleStatus)
            {
                case ToggleStatus.ToggledOff:
                    bikeMap.LandmarksEnabled = true;
                    if (bikeMap.ZoomLevel < MIN_ZOOMLEVEL_FOR_LANDMARKS)
                    {
                        bikeMap.ZoomLevel = MIN_ZOOMLEVEL_FOR_LANDMARKS;
                    }
                    landmarksToggleStatus = ToggleStatus.ToggledOn;
                    break;
                case ToggleStatus.ToggledOn:
                    bikeMap.LandmarksEnabled = false;
                    landmarksToggleStatus = ToggleStatus.ToggledOff;
                    break;
            }

        }

        #endregion

        #region Helper functions for App Bar button and menu item event handlers

        private void ShowLocation()
        {
            Ellipse myCircle = new Ellipse();
            myCircle.Fill = new SolidColorBrush(Colors.Orange);
            myCircle.Height = 30;
            myCircle.Width = 30;
            myCircle.Opacity = 100;

            MapOverlay myLocationOverlay = new MapOverlay();
            myLocationOverlay.Content = myCircle;
            myLocationOverlay.PositionOrigin = new Point(0.5, 0.5);
            myLocationOverlay.GeoCoordinate = currentLocation;

            locationLayer.Add(myLocationOverlay);
        }

        private void DrawBike(int id, GeoCoordinate location)
        {
            var image = new Image();
            image.Name = string.Format("bike_{0}", id.ToString());
            image.Width = 40;
            image.Height = 40;
            image.Opacity = 100;
            image.Source = new BitmapImage(new Uri("/Assets/sbike_small.png", UriKind.Relative));
            image.Tap += Bike_Tapped;

            MapOverlay bikeOverlay = new MapOverlay();
            bikeOverlay.Content = image;
            bikeOverlay.PositionOrigin = new Point(0.5, 0.5);
            bikeOverlay.GeoCoordinate = location;

            bikeLayer.Add(bikeOverlay);
        }

        private async void Bike_Tapped(object sender, GestureEventArgs e)
        {
            if(svcController.Bike == null)
            {
                int id = int.Parse(((Image)sender).Name.Split(new char[] { '_' })[1]);
                svcController.Bike = svcController.BikeList.Where(item => item.Id == id).FirstOrDefault();
                await svcController.ReserveBike();
                bikeMap.Layers.Remove(bikeLayer);
                bikeLayer = null;
            }
            else
            {
                MessageBox.Show("You already have a bike, please release it first before requesting a new one.");
            }
        }

        private async void FreeBike(object sender, EventArgs e)
        {
            await svcController.FreeBike();
            await RefreshBikes();
        }

        private async Task RefreshBikes()
        {
            bikeLayer = new MapLayer();
            await InitializeBikes();
            bikeMap.Layers.Add(bikeLayer);
        }

        private async void GetLocation()
        {
            Geolocator myGeolocator = new Geolocator();
            Geoposition myGeoposition = await myGeolocator.GetGeopositionAsync();
            Geocoordinate myGeocoordinate = myGeoposition.Coordinate;
            currentLocation = CoordinateConverter.ConvertGeocoordinate(myGeocoordinate);

            // hardcoding current location as GPS is not avaialble
            currentLocation = new GeoCoordinate(44.425579, 26.110166); // @ Biblioteca Nationala Bucuresti
        }

        private void CenterMapOnLocation()
        {
            bikeMap.Center = currentLocation;
        }

        #endregion

        private void BuildLocalizedApplicationBar()
        {
            ApplicationBar = new ApplicationBar();
            ApplicationBar.Opacity = 1;
            ApplicationBar.BackgroundColor = Colors.Orange;

            ApplicationBarIconButton appBarButton = new ApplicationBarIconButton(new Uri("/Assets/AppBar/location.png", UriKind.Relative));
            appBarButton.Text = AppResources.AppBarToggleLocationButtonText;
            appBarButton.Click += ToggleLocation;
            ApplicationBar.Buttons.Add(appBarButton);

            appBarButton = new ApplicationBarIconButton(new Uri("/Assets/AppBar/landmarks.png", UriKind.Relative));
            appBarButton.Text = AppResources.AppBarToggleLandmarksButtonText;
            appBarButton.Click += FreeBike;
            ApplicationBar.Buttons.Add(appBarButton);

            ApplicationBarMenuItem appBarMenuItem = new ApplicationBarMenuItem(AppResources.AppBarToggleLocationMenuItemText);
            appBarMenuItem.Click += ToggleLocation;
            ApplicationBar.MenuItems.Add(appBarMenuItem);

            appBarMenuItem = new ApplicationBarMenuItem(AppResources.AppBarToggleLandmarksMenuItemText);
            appBarMenuItem.Click += ToggleLandmarks;
            ApplicationBar.MenuItems.Add(appBarMenuItem);

        }

        private enum ToggleStatus
        {
            ToggledOff,
            ToggledOn
        }
    }
}
