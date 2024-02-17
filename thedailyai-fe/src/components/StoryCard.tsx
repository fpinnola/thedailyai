import CategoryLabel from "./CategoryLabel";
import PagedTextViewer from "./PagedTextViewer";
// import bookmarkFilled from '../assets/bookmark-filled.png'
// import bookmarkEmpty from '../assets/bookmark-empty.png'


const StoryCard = ({ title, summary, url, category }: { title: string, summary: string, url: string, category: string } ) => {

    return (
        <div className="slider-children">
            <div style={{
                justifyContent: 'center',
                alignItems: 'center',
                display: 'flex',
                height: '100%',
                flexDirection: 'column',
                padding: '0px 5px 0px 5px',
            }}>
                <div style={{
                    display: 'flex',
                    flexDirection: 'row',
                    width: '100%',
                    alignItems: 'center',
                    gap: 15,
                    justifyContent: 'center'
                }}>
                    <h4>{title}</h4>
                </div>
                <PagedTextViewer text={summary} charsPerPage={900} />
                <div style={{
                    display: 'flex',
                    flexDirection: 'row',
                    gap: 15,
                    alignItems: 'center'
                }}>
                    <CategoryLabel label={category} />
                    <a target="_blank" href={url}>Goto source</a>
                </div>
            </div>
        </div>
    )

}

export default StoryCard;