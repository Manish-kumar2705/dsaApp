# 🎯 DSA Mastery System

A comprehensive Data Structures & Algorithms learning platform with AI-powered guidance, seamless integration with Obsidian, Anki, and NotebookLM.

## 🚀 Features

- **AI-Powered Learning**: Get detailed explanations and feedback on your solutions
- **Pattern-Wise Organization**: Learn DSA concepts systematically
- **Seamless Integration**: Works with Obsidian, Anki, and NotebookLM
- **Progress Tracking**: Monitor your learning journey
- **Mobile Access**: Study anywhere, anytime

## 📱 Mobile Access

### **Deployed Version**

Access the app on any device: [Your Streamlit Cloud URL]

### **Local Development**

```bash
streamlit run ui_enhanced.py
```

## 🔧 Setup

### **1. Clone Repository**

```bash
git clone https://github.com/yourusername/dsa-mastery-system.git
cd dsa-mastery-system
```

### **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3. Configure Environment**

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
OBSIDIAN_VAULT=path/to/your/obsidian/vault
```

### **4. Run Locally**

```bash
streamlit run ui_enhanced.py
```

## 🌐 Deployment

### **Streamlit Cloud (Recommended)**

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub account
4. Select repository and deploy

### **Other Platforms**

- **Railway**: Connect GitHub repo
- **Render**: Deploy from GitHub
- **Heroku**: Use Procfile and requirements.txt

## 📚 Usage

### **Daily Workflow**

1. **Solve Problems**: Practice with AI guidance
2. **Generate Notes**: Get detailed explanations
3. **Export to Tools**: Send to Obsidian, Anki, NotebookLM
4. **Review**: Study flashcards and ask AI questions

### **Mobile Study**

- Access via web browser on any device
- Use Anki mobile app for flashcards
- Sync progress across devices

## 🔗 Integrations

- **📁 Obsidian**: Rich markdown notes
- **📚 Anki**: Spaced repetition flashcards
- **🤖 NotebookLM**: AI-powered study assistant

## 📊 Progress Tracking

- Pattern-wise completion
- Difficulty breakdown
- Study session planning
- Export status monitoring

## 🛠️ Development

### **File Structure**

```
dsa-mastery-system/
├── ui_enhanced.py          # Main Streamlit interface
├── dsa_system.py           # Core backend logic
├── ai_client.py            # AI API integration
├── anki_manager.py         # Anki integration
├── notebooklm_export.py    # NotebookLM export
├── config.py               # Configuration
├── requirements.txt        # Dependencies
└── .streamlit/             # Streamlit config
```

### **Adding New Features**

1. Update core logic in `dsa_system.py`
2. Add UI components in `ui_enhanced.py`
3. Test locally with `streamlit run ui_enhanced.py`
4. Deploy to cloud for mobile access

## 🎯 Learning Path

1. **Start with Easy Problems**: Build confidence
2. **Follow Pattern Order**: Systematic learning
3. **Use AI Guidance**: Get explanations and feedback
4. **Review Regularly**: Use Anki for spaced repetition
5. **Ask Questions**: Use NotebookLM for deep understanding

## 📞 Support

- **Issues**: Create GitHub issue
- **Features**: Submit pull request
- **Questions**: Check documentation

---

**Happy Learning! 🚀**
