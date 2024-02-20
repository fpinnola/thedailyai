// import { useState } from 'react';
import { Carousel } from 'react-responsive-carousel';
import 'react-responsive-carousel/lib/styles/carousel.min.css'; // requires a loader

import './customCarouselStyles.css';
import { useEffect, useState } from 'react';

const PagedTextViewer = ({ text, defaultCharsPerPage = 500 }: { text: string, defaultCharsPerPage?: number }) => {
  const [charsPerPage, setCharsPerPage] = useState(defaultCharsPerPage);

  // Adjust charsPerPage based on screen width
  useEffect(() => {
    const handleResize = () => {
      const screenWidth = window.innerWidth;
      // For example, if screen width is more than 768px, we assume it's a desktop
      if (screenWidth > 500) {
        // Set a larger charsPerPage for desktop
        setCharsPerPage(1500); // Adjust this value as needed
      } else {
        // Set the default (smaller) charsPerPage for mobile
        setCharsPerPage(defaultCharsPerPage);
      }
    };

    // Set the initial size on mount
    handleResize();

    // Add event listener for window resize
    window.addEventListener('resize', handleResize);

    // Cleanup event listener on component unmount
    return () => window.removeEventListener('resize', handleResize);
  }, [defaultCharsPerPage]);

  // Function to split the text into pages
  const getTextPages = (text: string) => {
    let pages = [];
    let startIndex = 0;

    while (startIndex < text.length) {
      let endIndex = Math.min(startIndex + charsPerPage, text.length);
      if (endIndex < text.length) {
        let lastSpaceIndex = text.lastIndexOf(' ', endIndex);
        let lastNewlineIndex = text.lastIndexOf('\n', endIndex);
        let cutIndex = Math.max(lastSpaceIndex, lastNewlineIndex);
        if (cutIndex <= startIndex) {
          cutIndex = endIndex;
        }
        pages.push(text.substring(startIndex, cutIndex + 1));
        startIndex = cutIndex + 1;
      } else {
        pages.push(text.substring(startIndex, endIndex));
        break;
      }
    }

    return pages;
  };

  const pages = getTextPages(text);
  if (pages.length === 1) {
    return (
      <div style={{padding: '10px'}}>
        {pages[0]}
      </div>
    )
  }
  return (
    <Carousel
      showArrows={false}
      infiniteLoop={false}
      showStatus={false}
      showIndicators={true}
      showThumbs={false}
      swipeable={true}
      emulateTouch={true}
      preventMovementUntilSwipeScrollTolerance={true}
    >
      {pages.map((page, index) => (
        <div key={index} style={{ whiteSpace: 'pre-wrap', padding: '10px', marginBottom: 20, height: 450 }}>
          {page}
        </div>
      ))}
    </Carousel>
  );
};

export default PagedTextViewer;
