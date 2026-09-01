// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import fs from 'node:fs';

const corpGrammar = JSON.parse(fs.readFileSync(new URL('./corp.tmLanguage.json', import.meta.url), 'utf-8'));

const githubRepo = process.env.GITHUB_REPOSITORY ? process.env.GITHUB_REPOSITORY.split('/')[1] : 'corp';
const githubOwner = process.env.GITHUB_REPOSITORY ? process.env.GITHUB_REPOSITORY.split('/')[0] : 'corp-plus-plus';
const isGitHubPages = Boolean(process.env.GITHUB_PAGES || process.env.GITHUB_ACTIONS);

// https://astro.build/config
export default defineConfig({
	site: process.env.SITE || `https://${githubOwner}.github.io`,
	base: process.env.BASE_PATH || (isGitHubPages ? `/${githubRepo}` : undefined),
	integrations: [
		starlight({
			title: 'Corp++',
			description: 'The Enterprise-Grade Systems Programming Language Where Architecture Meets Middle-Management Jargon',
			logo: {
				src: './src/assets/corp_logo.png',
			},
			social: [
				{ icon: 'github', label: 'GitHub', href: `https://github.com/${githubOwner}/${githubRepo}` }
			],
			customCss: [
				'./src/styles/custom.css'
			],
			expressiveCode: {
				shiki: {
					langs: [corpGrammar]
				},
				customLangs: [corpGrammar]
			},
			sidebar: [
				{
					label: 'Getting Started',
					items: [
						{ label: 'Executive Summary & Intro', slug: 'getting-started/introduction' },
						{ label: 'Installation & Standalone Binary', slug: 'getting-started/installation' },
						{ label: 'Your First Q3 Deliverable (Hello World)', slug: 'getting-started/hello-world' },
					],
				},
				{
					label: 'Core Language Concepts',
					items: [
						{ label: 'Program Lifecycle & Alignment', slug: 'core-concepts/program-lifecycle' },
						{ label: 'State, Core Competencies & Layoffs', slug: 'core-concepts/variables-and-memory' },
						{ label: 'Control Flow & Strategic Pivots', slug: 'core-concepts/control-flow' },
						{ label: 'Standard I/O & Town Hall Telemetry', slug: 'core-concepts/io-and-telemetry' },
					],
				},
				{
					label: 'Collaboration & Risk Management',
					items: [
						{ label: 'Delegates & Cross-Functional Work', slug: 'collaboration/delegates-and-functions' },
						{ label: 'Risk Mitigation & Error Handling', slug: 'collaboration/risk-management' },
					],
				},
				{
					label: 'Enterprise Tooling',
					items: [
						{ label: 'Corporate CLI (`corp`) Reference', slug: 'tooling/cli-reference' },
						{ label: 'The Boardroom REPL', slug: 'tooling/the-boardroom-repl' },
						{ label: 'Corporate VM & Bytecode Architecture', slug: 'tooling/compiler-and-vm' },
						{ label: 'Incident Reports & PIP Notices', slug: 'tooling/incident-reports-and-pips' },
					],
				},
				{
					label: 'Reference & Best Practices',
					items: [
						{ label: 'Complete Grammar Cheatsheet', slug: 'reference/grammar-cheatsheet' },
						{ label: 'Standard Library Modules', slug: 'reference/standard-library' },
						{ label: 'Enterprise Cookbooks & Patterns', slug: 'reference/cookbooks' },
					],
				},
			],
		}),
	],
});
