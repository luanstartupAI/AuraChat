import React from 'react';
import { LifeBuoy } from 'lucide-react';

// This can be a simple link or trigger a modal/page
// For now, let's make it a link that opens in a new tab

const SupportLink: React.FC = () => {
    const supportUrl = "mailto:suporte@aura.com"; // Replace with actual support email or URL

    return (
        <a 
            href={supportUrl}
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center px-4 py-2 text-sm font-medium rounded-md hover:bg-muted text-muted-foreground hover:text-foreground"
        >
            <LifeBuoy className="mr-3 h-5 w-5" />
            <span>Suporte</span>
        </a>
    );
};

export default SupportLink;

// How to integrate:
// 1. Import this component into your main layout/sidebar component.
// 2. Place it where you want the support link to appear (e.g., at the bottom of the sidebar).
// Example (in a hypothetical Sidebar component):
// import SupportLink from './SupportLink';
// ...
// <nav> ... menu items ... </nav>
// <div className="mt-auto p-4">
//     <SupportLink />
// </div>

