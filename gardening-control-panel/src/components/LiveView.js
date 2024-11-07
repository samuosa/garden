// LiveView.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';

const LiveView = ({ token }) => {
  const [imageSrc, setImageSrc] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true; // To prevent state updates on unmounted component
    let previousImageUrl = null;

    const fetchImage = async () => {
      setLoading(true);
      setError(null);
      console.log('Fetching image...');
      try {
        const response = await axios.get('http://192.168.178.127:5000/picture', { // Confirm the correct IP
          responseType: 'blob', // Important for handling binary data
          headers: {
            'Authorization': `Bearer ${token}`, // Ensure token is valid
          },
        });
        console.log(response);
        // Revoke previous object URL if exists
        if (previousImageUrl) {
          URL.revokeObjectURL(previousImageUrl);
        }

        const imageUrl = URL.createObjectURL(response.data);
        previousImageUrl = imageUrl;

        if (isMounted) {
          setImageSrc(imageUrl);
          setLoading(false);
        }
      } catch (err) {
        console.error('Error fetching image:', err);
        if (isMounted) {
          setError('Failed to fetch image.');
          setLoading(false);
        }
      }
      
    };

    fetchImage();

    // Set up an interval to refresh the image
    const interval = setInterval(fetchImage, 10000); // Refresh every 5 seconds

    return () => {
      isMounted = false;
      clearInterval(interval);
      // Revoke the last object URL when component unmounts
      if (previousImageUrl) {
        URL.revokeObjectURL(previousImageUrl);
      }
    };
  }, [token]); // Include token in dependencies if it can change

  return (
    <div>
      <h2>Live View</h2>
      {loading && <p>Loading image...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {imageSrc && !loading && !error && (
        <img src={imageSrc} alt="Live View" style={{ width: '100%', height: 'auto' }} />
      )}
    </div>
  );
};

export default LiveView;
