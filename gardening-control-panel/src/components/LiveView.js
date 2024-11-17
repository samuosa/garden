// LiveView.js

import React, { useEffect, useState } from "react";
import axios from "axios";

const LiveView = ({ token }) => {
  const [imageSrc, setImageSrc] = useState("");
  const [cachedImageSrc, setCachedImageSrc] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  let previousImageUrl = null;

  const fetchImage = async () => {
    setError(null);
    console.log("Fetching image...");
    try {
      const response = await axios.get("http://192.168.178.130:5000/picture", {
        responseType: "blob",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      console.log(response);
      if (previousImageUrl) {
        URL.revokeObjectURL(previousImageUrl);
      }

      const imageUrl = URL.createObjectURL(response.data);
      previousImageUrl = imageUrl;

      setCachedImageSrc(imageSrc || imageUrl); // Cache the current image before updating, use fetched image if none cached
      setImageSrc(imageUrl);
      setLoading(false);
    } catch (err) {
      console.error("Error fetching image:", err);
      setError("Failed to fetch image.");
      setLoading(false);
    }
  };

  useEffect(() => {
    let isMounted = true; // To prevent state updates on unmounted component

    fetchImage();

    const interval = setInterval(() => {
      setLoading(true);
      fetchImage();
    }, 100000);

    return () => {
      isMounted = false;
      clearInterval(interval);
      if (previousImageUrl) {
        URL.revokeObjectURL(previousImageUrl);
      }
    };
  }, [token]);

  const handleRefresh = () => {
    setLoading(true);
    setError(null);
    setCachedImageSrc(imageSrc); // Cache the current image
    fetchImage();
  };

  return (
    <div
      className="container d-flex justify-content-center align-items-center"
      style={{
        width: "100%",
        maxWidth: "600px", // Set the max width for the component
        aspectRatio: "16/9", // Enforces the 16:9 aspect ratio
        border: "1px solid #ddd",
        borderRadius: "8px",
        backgroundColor: "#f8f9fa",
        overflow: "hidden",
        position: "relative", // Ensures children elements respect container size
        cursor: imageSrc ? "pointer" : "default", // Change cursor to indicate image is clickable
      }}
    >
      <div
        style={{
          position: "absolute",
          bottom: "10px",
          right: "10px",
          zIndex: 3,
        }}
      >
        <button
          onClick={handleRefresh}
          style={{
            background: "none",
            border: "none",
            cursor: "pointer",
          }}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="currentColor"
            className="bi bi-arrow-clockwise"
            viewBox="0 0 16 16"
          >
            <path
              fillRule="evenodd"
              d="M8 3a5 5 0 1 1-4.546 2.914.5.5 0 1 0-.908-.418A6 6 0 1 0 8 2v1z"
            />
            <path d="M8 1a.5.5 0 0 1 .5.5v3a.5.5 0 0 1-1 0v-3A.5.5 0 0 1 8 1z" />
          </svg>
        </button>
      </div>
      <div
        className="text-center"
        style={{ width: "100%", height: "100%" }}
        onClick={() => {
          if (imageSrc) window.open(imageSrc, "_blank");
        }}
      >
        {cachedImageSrc && (
          <img
            src={cachedImageSrc}
            alt="Cached Live View"
            style={{
              width: "100%",
              height: "100%",
              objectFit: "contain", // Ensures the image fits within the aspect ratio without cropping
              position: "absolute", // Place it behind the loading spinner
              top: 0,
              left: 0,
              zIndex: 1, // Lower z-index to ensure spinner is above
            }}
          />
        )}
        {loading && (
          <div
            className="d-flex justify-content-center align-items-center direction-column"
            style={{
              height: "100%",
              width: "100%",
              position: "absolute",
              top: 0,
              left: 0,
              zIndex: 2, // Higher z-index to show loader over the cached image
              backgroundColor: "rgba(255, 255, 255, 0.5)", // Slightly transparent to indicate loading
            }}
          >
            <div className="spinner-border" role="status"></div>
            <p className="sr-only">Loading...</p>
          </div>
        )}
        {error && <p style={{ color: "red" }}>{error}</p>}
        {imageSrc && !loading && !error && (
          <img
            src={imageSrc}
            alt="Live View"
            style={{
              width: "100%",
              height: "100%",
              objectFit: "contain", // Ensures the image fits within the aspect ratio without cropping
              position: "absolute",
              top: 0,
              left: 0,
              zIndex: 1,
            }}
          />
        )}
      </div>
    </div>
  );
};

export default LiveView;
