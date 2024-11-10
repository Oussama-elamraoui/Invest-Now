// Toast.js
import React, { useEffect, useState } from 'react';
import '../style/toast.css';

const Toast = ({ type, message, show, onClose }) => {
  const [visible, setVisible] = useState(show);

  useEffect(() => {
    if (show) {
      setVisible(true);
      const timer = setTimeout(() => {
        setVisible(false);
        onClose();
      }, 3000); // Automatically hide after 3 seconds
      return () => clearTimeout(timer);
    }
  }, [show, onClose]);

  return (
    visible && (
      <div className={`toast toast-${type}`}>
        <p>{message}</p>
      </div>
    )
  );
};

export default Toast;
