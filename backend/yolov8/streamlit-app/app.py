# Python In-built packages
from pathlib import Path
import PIL

from PIL import Image

# External packages
import streamlit as st
import streamlit.components.v1 as components
# Local Modules
import settings
import helper

from streamlit_extras.switch_page_button import switch_page

# Setting page layout
st.set_page_config(
    page_title="Waste Classification using EcoVision 🍃",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("Waste Classification using EcoVision 🍃")

# Sidebar
st.sidebar.header("ML Model Config")

# Model Options
model_type = st.sidebar.radio(
    "Select Task", ['Detection'])

confidence = float(st.sidebar.slider (
    "Select Model Confidence", 25, 100, 40)) / 100

# Selecting Detection Or Segmentation
if model_type == 'Detection':
    model_path = Path(settings.DETECTION_MODEL)
elif model_type == 'Segmentation':
    model_path = Path(settings.SEGMENTATION_MODEL)

# Load Pre-trained ML Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST)

source_img = None
# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)     

    with col1:
        try:
            if source_img is None:
                default_image_path = "C:/Users/Hemanth/OneDrive/Desktop/GENESIS_CODE-RED-25/backend/yolov8/streamlit-app/images/def1.png"
                default_image = Image.open(default_image_path)
                st.image(default_image_path, caption="Default Image",
                         use_container_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image",
                         use_container_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = "C:/Users/Hemanth/OneDrive/Desktop/GENESIS_CODE-RED-25/backend/yolov8/streamlit-app/images/def1.png"
            default_detected_image = Image.open(
                default_detected_image_path)
            st.image(default_detected_image_path, caption='Detected Image',
                     use_container_width=True)
        else:
            if st.sidebar.button('Detect Objects'):
                res = model.predict(uploaded_image,
                                    conf=confidence
                                    )
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Detected Image',
                         use_container_width=True)
                
            
# If video is selected  

elif source_radio == settings.WEBCAM:
    helper.play_webcam(confidence, model)

else:
    st.error("Please select a valid source type!")

st.sidebar.header("Actions")
# Sidebar button to trigger the map
if st.sidebar.button("Facilities Near Me 🌍"):
    components.html(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"></script>
        </head>
        <body>
            <div id="map" style="height: 600px; width: 100%;"></div>
            <script>
                // Hardcoded marker locations (latitude, longitude)
                const markers = [
                    { name: "Plastic recycling facility", lat: 13.1339736, lon: 77.57775622 },
                    { name: "Metal recycling facility", lat: 13.1307467, lon: 77.5801217 },
                    { name: "Biodegradable & Recycling & Disposal facility", lat: 13.1315378, lon: 77.56651 },
                    { name: "Glass Recycling & Processing facility ", lat: 13.1540626, lon: 77.5678271 },
                    { name: "Plastic recycling facility", lat: 13.117041, lon: 77.5817156 },
                    { name: "Metal recycling facility", lat: 13.150592, lon: 77.5710312 },
                    { name: "Biodegradable & Recycling & Disposal facility", lat: 13.1501564, lon: 77.554581 },
                    { name: "Glass Recycling & Processing facility ", lat: 13.1125362, lon: 77.586302 },
                    { name: "Plastic recycling facility", lat: 13.0987631, lon: 77.5777261 },
                    { name: "Metal recycling facility", lat: 13.0977977, lon: 77.5842817 },
                    { name: "Biodegradable & Recycling & Disposal facility", lat: 13.1022468, lon: 77.5716997 },-
                    { name: "Glass Recycling & Processing facility ", lat: 13.1040904, lon: 77.5716596 },
                    { name: "Plastic recycling facility", lat: 13.1083895, lon: 77.5740354 },
                    { name: "Metal recycling facility", lat: 13.1062353, lon: 77.5721619 },
                    { name: "Biodegradable & Recycling & Disposal facility", lat: 13.0932472, lon: 77.5888943 },
                    { name: "Glass Recycling & Processing facility ", lat: 13.093793, lon: 77.5712636 },
                     { name: "Plastic recycling facility", lat: 13.121056, lon: 77.6121104 },
                    { name: "Metal recycling facility", lat: 13.1272207, lon: 77.5867729 },
                    { name: "Biodegradable & Recycling & Disposal facility", lat: 13.1475251, lon: 77.6375739 },
                    { name: "Glass Recycling & Processing facility ", lat: 13.0927381, lon: 77.587819 },
                    { name: "Plastic recycling facility", lat: 13.0632212, lon: 77.5592227 },
                    { name: "Metal recycling facility", lat: 13.0717094, lon: 77.5678536 },
                    { name: "Biodegradable & Recycling & Disposal facility", lat: 13.0436723, lon: 77.5674972 },
                    { name: "Glass Recycling & Processing facility ", lat: 13.0390311, lon: 77.5975494 },
                    { name: "Metal recycling facility", lat: 13.2096988, lon: 77.5459134 }
                ];

                // Function to calculate distance between two coordinates
                function calculateDistance(lat1, lon1, lat2, lon2) {
                    const R = 6371; // Radius of the Earth in km
                    const dLat = (lat2 - lat1) * Math.PI / 180;
                    const dLon = (lon2 - lon1) * Math.PI / 180;
                    const a = 
                        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                        Math.sin(dLon / 2) * Math.sin(dLon / 2);
                    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
                    return R * c; // Distance in km
                }

                // Initialize the map
                const map = L.map('map').setView([13.035, 77.59], 14); // Default center

                // Add OpenStreetMap tiles
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 18,
                    attribution: 'Map data © OpenStreetMap contributors'
                }).addTo(map);

                // Get user's location
                if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(
        function (position) {
            const userLat = position.coords.latitude;
            const userLon = position.coords.longitude;

            // Define a custom icon for the user's location using a local file
            const houseIcon = L.icon({
                iconUrl: 'backend\yolov8\streamlit-app\images\house.jpg', // Path to the local icon file
                iconSize: [32, 32], // Size of the icon
                iconAnchor: [16, 32], // Anchor point of the icon (bottom-center)
                popupAnchor: [0, -32] // Popup anchor point
            });

            // Add a marker for the user's location with the custom icon
            const userMarker = L.marker([userLat, userLon], { icon: houseIcon }).addTo(map);
            userMarker.bindPopup("You are here!").openPopup();

             const range = 15; // Show markers within 5 km

                    // Add markers for facilities within the specified range
                    markers.forEach(marker => {
                        const distance = calculateDistance(userLat, userLon, marker.lat, marker.lon).toFixed(2); // Distance in km
                        if (distance <= range) {
                            const facilityMarker = L.marker([marker.lat, marker.lon]).addTo(map);
                            facilityMarker.bindPopup(`${marker.name}<br>Distance: ${distance} km`);
                        }
                    });

            // Set the map view to the user's location
            map.setView([userLat, userLon], 14);
        },
        function (error) {
            alert("Unable to retrieve your location. Please enable location services and try again.");
        }
    );
}

 else {
                    alert("Geolocation is not supported by your browser.");
                }
            </script>
        </body>
        </html>
        """,
        height=600,
    )

st.sidebar.header("USEFUL LINKS")
st.sidebar.markdown("https://en.wikipedia.org/wiki/Swachh_Bharat_Mission")
st.sidebar.markdown("https://en.wikipedia.org/wiki/Waste_management_in_India")
st.sidebar.markdown("https://www.psa.gov.in/waste-to-wealth")
st.sidebar.markdown("https://cpcb.nic.in/national-action-plan/")
st.sidebar.markdown("https://sansad.in/getFile/BillsTexts/LSBillTexts/Asintroduced/37%20of%202023%20EV%20As%20Int84202372605PM.pdf")
st.sidebar.markdown("https://nskfdc.nic.in/en/system/files/Scheme%20guidelines%20of%20Waste%20Scheme..._compressed.pdf")




