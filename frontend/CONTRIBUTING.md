# Contributing to StyleAgent 🎨

Thank you for your interest in contributing to StyleAgent! We welcome contributions from developers, designers, and fashion enthusiasts.

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Git
- Basic knowledge of React, TypeScript, and Tailwind CSS

### Development Setup
1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/StyleAgent.git`
3. Install dependencies: `npm install`
4. Start development server: `npm run dev`
5. Open `http://localhost:5173` in your browser

## 📋 How to Contribute

### 🐛 Bug Reports
- Use the GitHub issue tracker
- Include steps to reproduce
- Provide browser/OS information
- Add screenshots if applicable

### ✨ Feature Requests
- Check existing issues first
- Describe the feature clearly
- Explain the use case and benefits
- Consider implementation complexity

### 🔧 Code Contributions

#### Branch Naming
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

#### Code Style
- Follow existing TypeScript/React patterns
- Use Tailwind CSS for styling
- Maintain responsive design principles
- Add proper TypeScript types
- Include JSDoc comments for complex functions

#### Component Guidelines
- Keep components under 200 lines
- Use proper separation of concerns
- Follow the existing file structure
- Add proper prop types and interfaces

### 🎨 Design Contributions
- Follow Apple-level design aesthetics
- Maintain consistent spacing (8px system)
- Use the existing color palette
- Ensure mobile-first responsive design
- Add smooth animations and micro-interactions

### 📝 Documentation
- Update README.md for new features
- Add inline code comments
- Update TypeScript interfaces
- Include usage examples

## 🧪 Testing

### Before Submitting
- [ ] Code builds without errors (`npm run build`)
- [ ] No TypeScript errors (`npm run lint`)
- [ ] Responsive design works on mobile/desktop
- [ ] All animations are smooth
- [ ] Accessibility standards maintained

### Manual Testing Checklist
- [ ] Chat interface flows correctly
- [ ] Image upload works with drag-and-drop
- [ ] Loading states display properly
- [ ] Recommendations render correctly
- [ ] Social sharing functions work
- [ ] Reset functionality works

## 📦 Pull Request Process

1. **Create a descriptive PR title**
   - `feat: add social media sharing functionality`
   - `fix: resolve mobile layout issues`
   - `docs: update installation instructions`

2. **Fill out the PR template**
   - Describe changes made
   - Link related issues
   - Add screenshots for UI changes
   - List breaking changes if any

3. **Code Review Process**
   - Maintainers will review within 48 hours
   - Address feedback promptly
   - Keep discussions constructive
   - Be open to suggestions

## 🏗️ Architecture Guidelines

### File Structure
```
src/
├── components/          # Reusable UI components
├── hooks/              # Custom React hooks
├── types/              # TypeScript type definitions
├── utils/              # Utility functions
├── styles/             # Global styles
└── App.tsx             # Main application component
```

### Component Organization
- One component per file
- Co-locate related components
- Use index.ts for clean imports
- Keep components focused and reusable

### State Management
- Use React hooks for local state
- Consider Context API for global state
- Avoid prop drilling
- Keep state close to where it's used

## 🎯 Priority Areas

### High Priority
- Backend API integration
- Computer vision implementation
- RAG pipeline development
- Performance optimizations

### Medium Priority
- Additional outfit categories
- Enhanced filtering options
- User authentication
- Favorites functionality

### Low Priority
- Dark mode support
- Internationalization
- Advanced animations
- PWA features

## 🤝 Community Guidelines

### Be Respectful
- Use inclusive language
- Respect different perspectives
- Provide constructive feedback
- Help newcomers learn

### Communication
- Use GitHub issues for technical discussions
- Tag maintainers when needed
- Be patient with response times
- Ask questions if unclear

## 🏆 Recognition

Contributors will be:
- Added to the README contributors section
- Mentioned in release notes
- Invited to join the core team (for significant contributions)

## 📞 Getting Help

- **GitHub Issues**: Technical questions and bugs
- **Discussions**: General questions and ideas
- **Email**: styleagent.team@example.com

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping make StyleAgent better! 🙏**