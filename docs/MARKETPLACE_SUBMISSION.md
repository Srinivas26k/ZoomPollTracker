# Zoom Marketplace Submission Guide

This document provides guidance for submitting the Real-Time Zoom Poll Automation application to the Zoom Marketplace.

## Prerequisites

Before submitting to the Zoom Marketplace, ensure you have:

1. A completed, fully tested application
2. A Zoom Developer account
3. All required documentation
4. Graphics and branding materials
5. Privacy policy and terms of service

## Zoom App Types

For this application, you'll be creating a **Server-to-Server OAuth** app type. This allows your application to interact with the Zoom API without requiring user authentication for each API call.

## Step 1: Prepare Your Application

Ensure your application meets all requirements:

- Application runs stably on Windows (primary platform)
- All features are tested and working
- Error handling is robust
- Documentation is complete
- Local AI model integration works as expected
- Zoom API integration is functioning properly

## Step 2: Required App Information

You'll need to provide the following information during submission:

### Basic Information
- App name: "Real-Time Zoom Poll Automation"
- Short description (80 chars max): "Automated poll generation during meetings based on real-time content analysis"
- Long description (200 words max): "This application automatically generates relevant polls during Zoom meetings based on real-time content analysis. Using advanced AI models, it listens to meeting discussions and creates contextually appropriate polls to gather feedback and improve engagement. Supports both cloud-based AI (OpenAI) and local models (Ollama) for maximum flexibility and privacy."
- Developer name: [Your name/company]
- Developer email: [Your email]
- Support URL: [Your support page URL]
- Privacy policy URL: [Your privacy policy URL]
- Terms of service URL: [Your terms of service URL]

### Features & Functionality
- Primary category: "Meeting Enhancement"
- Secondary category: "Productivity"
- Tags: "polls", "AI", "automation", "engagement", "feedback"

### Distribution 
- Is this app published to other marketplaces? No
- Is this app available as an integration for other platforms? No

## Step 3: Prepare Required Assets

### Screenshots (at least 3)
1. Main application dashboard
2. Poll generation settings
3. AI model selection screen
4. Active poll display
5. Analytics view (optional)

### App Icon
- Size: 512x512 pixels
- Format: PNG
- Background: Transparent or solid
- The icon should be recognizable even at small sizes

### App Logo
- Size: 1024x512 pixels
- Format: PNG
- Background: Should match your branding

### Feature Video (Optional but Recommended)
- Length: 1-3 minutes
- Format: MP4 or YouTube link
- Content: Demonstrate key features and benefits

## Step 4: Configure OAuth Scopes

For a Server-to-Server OAuth app, you'll need to specify the scopes required by your application:

- `meeting:read:admin` - To get meeting information
- `meeting:write:admin` - To create and manage polls
- `meeting:master` - For complete meeting management

## Step 5: Technical Requirements

Ensure you've implemented:

1. Proper error handling for all API calls
2. Rate limiting compliance (respecting Zoom's API rate limits)
3. Secure storage of authentication tokens
4. Data handling in compliance with privacy laws

## Step 6: Testing Requirements

Before submission, test the following scenarios:

1. **Happy Path Testing**
   - Starting a meeting and connecting the app
   - Automatic poll generation
   - Changing AI models and settings
   - Exporting data

2. **Error Path Testing**
   - Handling API errors
   - Recovery from network interruptions
   - Graceful degradation when features are unavailable

3. **Performance Testing**
   - Memory usage over time
   - CPU utilization during transcription
   - Response times for poll generation

## Step 7: Submission Process

1. Log in to the [Zoom App Marketplace](https://marketplace.zoom.us/)
2. Go to "Develop" > "Build App"
3. Select "Server-to-Server OAuth" as your app type
4. Fill in all required information from Steps 2-5
5. Upload all assets from Step 3
6. Submit for review

## Step 8: Review Process

After submission, Zoom will review your application. The review process typically takes 7-10 business days.

You may receive feedback requesting changes before approval. Common feedback includes:

- Security concerns
- UI/UX improvements
- Documentation clarity
- API usage optimizations

## Step 9: Post-Approval

Once approved:

1. Announce your app's availability
2. Monitor usage and gather feedback
3. Plan for updates and improvements
4. Maintain compliance with Zoom's policies

## Requirements Checklist

Use this checklist to ensure your submission is complete:

- [ ] Application fully tested and functional
- [ ] All required information compiled
- [ ] Screenshots, icons, and logos prepared
- [ ] OAuth scopes properly configured
- [ ] Technical requirements implemented
- [ ] Testing completed across all scenarios
- [ ] Documentation complete and accurate
- [ ] Privacy policy and terms of service ready

## Additional Resources

- [Zoom App Marketplace](https://marketplace.zoom.us/)
- [Zoom App Developer Guide](https://developers.zoom.us/docs/apps/)
- [Server-to-Server OAuth](https://developers.zoom.us/docs/internal-apps/s2s-oauth/)
- [Zoom API Reference](https://developers.zoom.us/docs/api/rest/reference/)
- [Zoom Support](https://support.zoom.us/)

## Contact Information

If you have questions about the marketplace submission process:

- Email: [marketplace@zoom.us](mailto:marketplace@zoom.us)
- Developer Support: [https://developers.zoom.us/support](https://developers.zoom.us/support)