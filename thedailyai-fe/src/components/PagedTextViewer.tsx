// import { useState } from 'react';
import { Carousel } from 'react-responsive-carousel';
import 'react-responsive-carousel/lib/styles/carousel.min.css'; // requires a loader

import './customCarouselStyles.css';

const PagedTextViewer = ({ text, charsPerPage = 500 }: { text: string, charsPerPage?: number }) => {
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
