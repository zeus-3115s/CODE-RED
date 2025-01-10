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

confidence = float(st.sidebar.slider(
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
                default_image_path = "C:/Users/Hemanth/OneDrive/Desktop/GENESIS_CODE-RED-25-main/backend/yolov8/streamlit-app/images/def1.png"
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
            default_detected_image_path = "C:/Users/Hemanth/OneDrive/Desktop/GENESIS_CODE-RED-25-main/backend/yolov8/streamlit-app/images/def1.png"
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

# Function to Display Map
def show_map():
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
                const markers = [
                    { name: "Plastic recycling facility", lat: 13.1339736, lon: 77.57775622 },
                    { name: "Metal recycling facility", lat: 13.1307467, lon: 77.5801217 },
                    { name: "Biodegradable & Recycling & Disposal facility", lat: 13.1315378, lon: 77.56651 },
                    { name: "Glass Recycling & Processing facility ", lat: 13.1540626, lon: 77.5678271 }
                ];

                function calculateDistance(lat1, lon1, lat2, lon2) {
                    const R = 6371;
                    const dLat = (lat2 - lat1) * Math.PI / 180;
                    const dLon = (lon2 - lon1) * Math.PI / 180;
                    const a =
                        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                        Math.sin(dLon / 2) * Math.sin(dLon / 2);
                    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
                    return R * c;
                }

                const map = L.map('map').setView([13.035, 77.59], 14);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 18,
                    attribution: 'Map data © OpenStreetMap contributors'
                }).addTo(map);

                if ("geolocation" in navigator) {
                    navigator.geolocation.getCurrentPosition(
                        function (position) {
                            const userLat = position.coords.latitude;
                            const userLon = position.coords.longitude;

                            const userMarker = L.marker([userLat, userLon]).addTo(map);
                            userMarker.bindPopup("You are here!").openPopup();

                            const range = 10;
                            markers.forEach(marker => {
                                const distance = calculateDistance(userLat, userLon, marker.lat, marker.lon).toFixed(2);
                                if (distance <= range) {
                                    const facilityMarker = L.marker([marker.lat, marker.lon]).addTo(map);
                                    facilityMarker.bindPopup(`${marker.name}<br>Distance: ${distance} km`);
                                }
                            });

                            map.setView([userLat, userLon], 14);
                        },
                        function (error) {
                            alert("Unable to retrieve your location.");
                        }
                    );
                } else {
                    alert("Geolocation is not supported by your browser.");
                }
            </script>
        </body>
        </html>
        """,
        height=600,
    )

# Sidebar button to trigger the map
if st.sidebar.button("Facilities Near Me 🌍"):
    show_map()
    # components.html(
    #     """
    #     <!DOCTYPE html>
    #     <html>
    #     <head>
    #         <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css" />
    #         <script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"></script>
    #     </head>
    #     <body>
    #         <div id="map" style="height: 600px; width: 100%;"></div>
    #         <script>
    #             const markers = [
    #                 { name: "Plastic recycling facility", lat: 13.1339736, lon: 77.57775622 },
    #                 { name: "Metal recycling facility", lat: 13.1307467, lon: 77.5801217 },
    #                 { name: "Biodegradable & Recycling & Disposal facility", lat: 13.1315378, lon: 77.56651 },
    #                 { name: "Glass Recycling & Processing facility ", lat: 13.1540626, lon: 77.5678271 }
    #             ];

    #             function calculateDistance(lat1, lon1, lat2, lon2) {
    #                 const R = 6371;
    #                 const dLat = (lat2 - lat1) * Math.PI / 180;
    #                 const dLon = (lon2 - lon1) * Math.PI / 180;
    #                 const a =
    #                     Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    #                     Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    #                     Math.sin(dLon / 2) * Math.sin(dLon / 2);
    #                 const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    #                 return R * c;
    #             }

    #             const map = L.map('map').setView([13.035, 77.59], 14);
    #             L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    #                 maxZoom: 18,
    #                 attribution: 'Map data © OpenStreetMap contributors'
    #             }).addTo(map);

    #             if ("geolocation" in navigator) {
    #                 navigator.geolocation.getCurrentPosition(
    #                     function (position) {
    #                         const userLat = position.coords.latitude;
    #                         const userLon = position.coords.longitude;

    #                         const userMarker = L.marker([userLat, userLon]).addTo(map);
    #                         userMarker.bindPopup("You are here!").openPopup();

    #                         const range = 10;
    #                         markers.forEach(marker => {
    #                             const distance = calculateDistance(userLat, userLon, marker.lat, marker.lon).toFixed(2);
    #                             if (distance <= range) {
    #                                 const facilityMarker = L.marker([marker.lat, marker.lon]).addTo(map);
    #                                 facilityMarker.bindPopup(`${marker.name}<br>Distance: ${distance} km`);
    #                             }
    #                         });

    #                         map.setView([userLat, userLon], 14);
    #                     },
    #                     function (error) {
    #                         alert("Unable to retrieve your location.");
    #                     }
    #                 );
    #             } else {
    #                 alert("Geolocation is not supported by your browser.");
    #             }
    #         </script>
    #     </body>
    #     </html>
    #     """,
    #     height=600,
    # )
