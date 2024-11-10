import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const usePageTitle = (titleMap) => {
  const location = useLocation();

  useEffect(() => {
    const path = location.pathname;
    const newTitle = titleMap[path] || 'Default Title';
    document.title = newTitle;
  }, [location, titleMap]);
};

export default usePageTitle;
