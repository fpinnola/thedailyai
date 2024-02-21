import { addUserEngagement } from "../external/news_be.external";
import CategoryLabel from "./CategoryLabel";
import PagedTextViewer from "./PagedTextViewer";

import ThumbsUpEmpty from '../assets/thumbs-up-empty.png';
import ThumbsUpFilled from '../assets/thumbs-up-filled.png';
import ThumbsDownEmpty from '../assets/thumbs-down-empty.png';
import ThumbsDownFilled from '../assets/thumbs-down-filled.png';
import { useState } from "react";
import ImageButton from "./ImageButton";


const StoryCard = ({ title, summary, url, category, dateString, articleId }: { title: string, summary: string, url: string, category: string, dateString: string, articleId: string } ) => {

    const [thumbsUpSelected, setThumbsUpSelected] = useState(false);
    const [thumbsDownSelected, setThumbsDownSelected] = useState(false);

    function formatDate(dateString: string) {
        const date = new Date(dateString);
        const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: '2-digit' };
        if (!options) return '';
        return new Intl.DateTimeFormat('en-US', options).format(date);
    }

    function handleAction(action: string) {
        addUserEngagement(articleId, action);
    }

    function toggleRating(thumbsUp: boolean) {
        if (thumbsUp) {
            if (thumbsUpSelected) {
                setThumbsUpSelected(false);
            } else {
                setThumbsUpSelected(true);
                setThumbsDownSelected(false);
                handleAction("thumbs-up");
            }
        } else {
            if (thumbsDownSelected) {
                setThumbsDownSelected(false);
            } else {
                setThumbsDownSelected(true);
                setThumbsUpSelected(false);
                handleAction("thumbs-down");
            }
        }
    }

    return (
        <div className="slider-children">
            <div style={{
                justifyContent: 'center',
                alignItems: 'center',
                display: 'flex',
                height: '100%',
                flexDirection: 'column',
                padding: '0px 2px 0px 2px',
            }}>
                <h4 style={{ marginBottom: 5}}>{title}</h4>
                <h5 style={{ marginTop: 2 }}>{formatDate(dateString)}</h5>
                <PagedTextViewer text={summary} defaultCharsPerPage={600} />
                <div style={{
                    display: 'flex',
                    flexDirection: 'row',
                    gap: 15,
                    alignItems: 'center'
                }}>
                    {thumbsUpSelected ? (
                    <ImageButton imageSize={{height: 24, width: 24}} onClick={() => toggleRating(true)} image={ThumbsUpFilled} />) :
                    (<ImageButton imageSize={{height: 24, width: 24}} onClick={() => toggleRating(true)} image={ThumbsUpEmpty} />)}
                    {thumbsDownSelected ? (
                    <ImageButton imageSize={{height: 24, width: 24}} onClick={() => toggleRating(false)} image={ThumbsDownFilled} />) :
                    (<ImageButton imageSize={{height: 24, width: 24}} onClick={() => toggleRating(false)} image={ThumbsDownEmpty} />)}
                    <CategoryLabel label={category} />
                    <a target="_blank" onClick={() => handleAction("goto-source")} href={url}>Goto source</a>
                </div>
            </div>
        </div>
    )

}

export default StoryCard;