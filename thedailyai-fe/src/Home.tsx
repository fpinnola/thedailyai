import { useEffect, useState } from "react";

const SAMPLE_ARTICLES = [
    { title: 'Flying Cars to Become Mainstream by 2025', url: 'https://example.com/flying-cars-2025', summary: 'Industry experts predict flying cars will dominate city skies in the next year.' },
    { title: 'Scientists Discover Water on the Sun', url: 'https://example.com/water-on-sun', summary: 'A groundbreaking discovery reveals large bodies of water on the sun’s surface.' },
    { title: 'World’s First Time Machine Built in Secret', url: 'https://example.com/first-time-machine', summary: 'Sources claim a fully functional time machine has been created in a private lab.' },
    { title: 'Dinosaurs Found Alive in Remote Jungle', url: 'https://example.com/dinosaurs-alive', summary: 'Explorers uncover a hidden ecosystem where dinosaurs continue to thrive.' },
    { title: 'Global Internet to Shut Down for Maintenance', url: 'https://example.com/global-internet-shutdown', summary: 'Authorities announce a scheduled global internet shutdown for system upgrades.' }
]

const SAMPLE_BROADCAST = "Good evening, tech enthusiasts! You're listening to the Daily Tech Update with me, Jordan Lee. Let's get right into today's most exciting tech news. First up, big news from the tech world: FutureTech just unveiled its latest marvel, the FuturePhone X5. This new smartphone is a tech-lover's dream, featuring an AI-powered camera and a stunning transparent OLED display. But that's not all – the battery life is a game changer, promising days of use on a single charge. At the launch event earlier today, the buzz was all about these groundbreaking features, especially that AI camera which adapts to any lighting for the perfect shot. Now, let's switch gears to virtual reality. VirtualTech has introduced the DreamScape VR headset, and let me tell you, it's a breakthrough in immersive technology. I had the chance to try it out, and it's like stepping into a completely different world. It’s wireless, with no external sensors, offering a level of immersion that's simply unprecedented. This could really shake things up in the entertainment world. In cybersecurity news, there’s a serious development to talk about. Hackbots, a major player in security software, reported a significant data breach. This breach has compromised the personal data of millions. They’re ramping up security measures and working with law enforcement to get to the bottom of this. For all of us, it's a reminder to stay vigilant – update those passwords and enable two-factor authentication wherever possible. Finally, in a blend of tech and art, an AI-powered robot named Arti has been creating waves in the art world. Arti’s paintings, which merge traditional techniques with AI algorithms, are challenging our very notions of art and creativity. These pieces are set to be exhibited in New York next month, and they're already sparking a lot of conversations about the role of AI in art. That's all for today's Daily Tech Update. Tune in tomorrow for more of the latest and greatest in the world of technology. This is Jordan Lee, signing off. Have a tech-tastic evening!";

export default function Home() {

    const [articles, setArticles] = useState<any[]>([]);

    const [podcastScript, setPodcastScript] = useState('');

    useEffect(() => {
        // TODO: get articles from backend
        setArticles(SAMPLE_ARTICLES);
        setPodcastScript(SAMPLE_BROADCAST);
    }, []);

    const getDate = () => {
        const months = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"];
        const now = new Date();
        const month = months[now.getMonth()];
        const day = now.getDate();
        const year = now.getFullYear();

        return `${month} ${day}, ${year}`;
    }

    return (
        <>
            <h3>Your News for {getDate()}</h3>
            <div>
                {articles.map((elem) => (
                    <div>
                        <h4>{elem.title}</h4>
                        <p>{elem.summary}</p>
                        <a href={elem.url}>Read more</a>
                    </div>
                ) )}
            </div>
        </>
    )
}