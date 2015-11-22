using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Device.Location;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SmartBike.Models
{
    class Bike : INotifyPropertyChanged
    {
        private int m_id;
        private GeoCoordinate m_location;
        private bool m_free;
        private bool m_damaged;

        public Bike(int id, GeoCoordinate location)
        {
            Id = id;
            Free = true;
            Location = location;
        }

        public bool Free
        {
            get
            {
                return m_free;
            }

            set
            {
                m_free = value;
                OnPropertyChanged("Free");
            }
        }

        public int Id
        {
            get
            {
                return m_id;
            }

            set
            {
                m_id = value;
            }
        }

        public GeoCoordinate Location
        {
            get
            {
                return m_location;
            }

            set
            {
                m_location = value;
                OnPropertyChanged("Location");
            }
        }

        public bool Damaged
        {
            get
            {
                return m_damaged;
            }

            set
            {
                m_damaged = value;
                OnPropertyChanged("Damaged");
            }
        }

        public event PropertyChangedEventHandler PropertyChanged;
        public virtual void OnPropertyChanged(string propertyName)
        {
            PropertyChangedEventHandler handler = PropertyChanged;
            if (handler != null)
            {
                var e = new PropertyChangedEventArgs(propertyName);
                handler(this, e);
            }
        }

    }
}
