import { addUserEngagement } from "../external/news_be.external";
import CategoryLabel from "./CategoryLabel";
import PagedTextViewer from "./PagedTextViewer";



const StoryCard = ({ title, summary, url, category, dateString, articleId }: { title: string, summary: string, url: string, category: string, dateString: string, articleId: string } ) => {

    function formatDate(dateString: string) {
        const date = new Date(dateString);
        const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: '2-digit' };
        if (!options) return '';
        return new Intl.DateTimeFormat('en-US', options).format(date);
    }

    function handleAction(action: string) {
        addUserEngagement(articleId, action);
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
                <PagedTextViewer text={summary} charsPerPage={700} />
                <div style={{
                    display: 'flex',
                    flexDirection: 'row',
                    gap: 15,
                    alignItems: 'center'
                }}>
                    <CategoryLabel label={category} />
                    <a target="_blank" onClick={() => handleAction("goto-source")} href={url}>Goto source</a>
                </div>
            </div>
        </div>
    )

}

export default StoryCard;