# 📱 Mobile Authentication Guide

## 🎯 **How Mobile Authentication Works**

**Good news! You don't need to login through a terminal on your phone.** The mobile app uses environment variables and secrets that are configured once and work automatically.

---

## 🔐 **Authentication Methods**

### **Method 1: Streamlit Cloud Secrets (Recommended)**

- **How it works**: Configure once in Streamlit Cloud dashboard
- **Mobile access**: Automatically available on your phone
- **Security**: Encrypted and secure
- **No terminal needed**: Everything works through the web interface

### **Method 2: Environment Variables**

- **How it works**: Set up on your PC, syncs to mobile
- **Mobile access**: Inherits from PC configuration
- **Security**: Standard environment variable security

---

## 🚀 **Step-by-Step Mobile Setup**

### **Step 1: GitHub Authentication**

#### **Option A: Personal Access Token (Recommended)**

1. **Go to GitHub.com** on your phone or PC
2. **Navigate to**: Settings → Developer settings → Personal access tokens → Tokens (classic)
3. **Generate new token**:

   - Click "Generate new token (classic)"
   - Give it a name like "DSA Mastery Mobile"
   - Select scopes: `repo`, `workflow`
   - Copy the token (you'll only see it once!)

4. **Add to Streamlit Cloud**:
   - Go to your Streamlit Cloud dashboard
   - Find your app → Settings → Secrets
   - Add this secret:
   ```toml
   GITHUB_TOKEN = "your_token_here"
   GITHUB_REPO = "your-username/dsa-notes"
   ```

#### **Option B: GitHub App (Advanced)**

1. **Create GitHub App** on GitHub.com
2. **Configure permissions**: Repository access
3. **Generate private key**
4. **Add to Streamlit secrets**

### **Step 2: Google Drive Authentication**

#### **Option A: Service Account (Recommended)**

1. **Go to Google Cloud Console** on your PC
2. **Create a new project** or select existing
3. **Enable Google Drive API**
4. **Create Service Account**:

   - Go to IAM & Admin → Service Accounts
   - Click "Create Service Account"
   - Name it "DSA Mastery Mobile"
   - Grant "Editor" role

5. **Download JSON credentials**:

   - Click on the service account
   - Go to "Keys" tab
   - Add new key → JSON
   - Download the JSON file

6. **Add to Streamlit Cloud**:
   ```toml
   GDRIVE_CREDENTIALS = '''
   {
     "type": "service_account",
     "project_id": "your-project",
     "private_key_id": "...",
     "private_key": "...",
     "client_email": "...",
     "client_id": "...",
     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
     "token_uri": "https://oauth2.googleapis.com/token",
     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
     "client_x509_cert_url": "..."
   }
   '''
   GDRIVE_FOLDER_ID = "your_folder_id_here"
   ```

#### **Option B: OAuth2 (User-friendly)**

1. **Create OAuth2 credentials** in Google Cloud Console
2. **Configure consent screen**
3. **Add authorized redirect URIs**:
   - `https://your-app.streamlit.app/_stcore/authorize`
4. **Add to Streamlit secrets**:
   ```toml
   GOOGLE_CLIENT_ID = "your_client_id"
   GOOGLE_CLIENT_SECRET = "your_client_secret"
   ```

### **Step 3: NotebookLM Integration**

#### **Option A: Google Drive Sync (Recommended)**

- **Uses the same Google Drive credentials** from Step 2
- **No additional setup needed**
- **Automatic sync** to NotebookLM

#### **Option B: Webhook Integration**

1. **Get NotebookLM webhook URL** from your NotebookLM settings
2. **Add to Streamlit secrets**:
   ```toml
   NOTEBOOKLM_WEBHOOK_URL = "your_webhook_url"
   ```

#### **Option C: API Integration**

1. **Get NotebookLM API key** from your NotebookLM settings
2. **Add to Streamlit secrets**:
   ```toml
   NOTEBOOKLM_API_KEY = "your_api_key"
   ```

---

## 📱 **Mobile App Access**

### **Once Configured:**

1. **Open your Streamlit app** on your phone
2. **All authentication is automatic**
3. **No login prompts** on mobile
4. **Direct access** to all features

### **Mobile Features Available:**

- ✅ **GitHub upload** - One-click upload to your repository
- ✅ **Google Drive sync** - Automatic sync to your Drive folder
- ✅ **NotebookLM export** - Direct export to NotebookLM
- ✅ **Note generation** - AI-powered notes with your credentials
- ✅ **Flashcard creation** - Automatic Anki integration

---

## 🔧 **Troubleshooting**

### **"Authentication Failed" Error**

1. **Check Streamlit secrets** are correctly set
2. **Verify token permissions** (GitHub tokens need `repo` scope)
3. **Check folder permissions** (Google Drive folder must be accessible)
4. **Restart the app** after changing secrets

### **"Permission Denied" Error**

1. **GitHub**: Ensure token has `repo` and `workflow` permissions
2. **Google Drive**: Check service account has access to the folder
3. **NotebookLM**: Verify API key or webhook URL is correct

### **"Not Found" Error**

1. **GitHub**: Check repository name is correct
2. **Google Drive**: Verify folder ID is correct
3. **NotebookLM**: Ensure webhook/API endpoint is accessible

---

## 🛡️ **Security Best Practices**

### **Token Security:**

- ✅ **Use environment variables** or Streamlit secrets
- ✅ **Never commit tokens** to your code
- ✅ **Use minimal permissions** (only what's needed)
- ✅ **Rotate tokens regularly** (every 90 days)

### **Access Control:**

- ✅ **Limit repository access** to specific repos
- ✅ **Use service accounts** for automated access
- ✅ **Monitor usage** through GitHub/Google Cloud logs

---

## 📋 **Quick Setup Checklist**

### **For GitHub:**

- [ ] Create Personal Access Token
- [ ] Add `GITHUB_TOKEN` to Streamlit secrets
- [ ] Add `GITHUB_REPO` to Streamlit secrets
- [ ] Test upload from mobile

### **For Google Drive:**

- [ ] Create Google Cloud project
- [ ] Enable Google Drive API
- [ ] Create service account
- [ ] Download JSON credentials
- [ ] Add credentials to Streamlit secrets
- [ ] Add `GDRIVE_FOLDER_ID` to Streamlit secrets
- [ ] Test sync from mobile

### **For NotebookLM:**

- [ ] Choose sync method (Drive/Webhook/API)
- [ ] Configure credentials
- [ ] Add to Streamlit secrets
- [ ] Test export from mobile

---

## 🎉 **You're Ready!**

**Once configured:**

1. **Open your app** on mobile
2. **Solve problems** with AI guidance
3. **Generate notes** automatically
4. **Sync to all services** with one click
5. **Study with NotebookLM** - zero manual work!

**No terminal login needed on mobile - everything works through the web interface! 🚀📱**
