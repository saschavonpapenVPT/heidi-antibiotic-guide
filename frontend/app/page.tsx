'use client'

import { useState } from 'react'

export default function Home() {
  const [inputText, setInputText] = useState('')
  const [response, setResponse] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async () => {
    if (!inputText.trim()) {
      alert('Please enter some medical information first.')
      return
    }

    setIsLoading(true)
    setResponse('')

    try {
      // Connect directly to backend running on port 8004
      const apiUrl = 'http://localhost:8004'
      const response = await fetch(`${apiUrl}/ask-heidi`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: inputText
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      // Format the response to show the Heidi analysis nicely
      let formattedResponse = `${data.message}\n\n`
      
      if (data.extracted_drugs && data.extracted_drugs.length > 0) {
        formattedResponse += `💊 Extracted Drugs: ${data.extracted_drugs.join(', ')}\n\n`
      } else {
        formattedResponse += `💊 Extracted Drugs: None identified\n\n`
      }
      
      if (data.vector_context && data.vector_context.length > 0) {
        formattedResponse += `📚 Found ${data.vector_context.length} relevant reference chunks\n\n`
      }
      
      if (data.final_summary) {
        formattedResponse += `🧠 Heidi's Clinical Summary:\n${data.final_summary}\n\n`
      }
      
      if (data.processing_steps && data.processing_steps.length > 0) {
        formattedResponse += `⚙️ Processing Steps:\n`
        data.processing_steps.forEach((step, index) => {
          formattedResponse += `${index + 1}. ${step}\n`
        })
      }
      
      setResponse(formattedResponse)
      console.log('Backend response:', data)
      
    } catch (error) {
      console.error('Error calling backend:', error)
      setResponse('Error: Failed to connect to backend API')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main style={{
      minHeight: '100vh',
      backgroundColor: '#f9fafb',
      padding: '2rem'
    }}>
      {/* Header */}
      <div style={{
        textAlign: 'center',
        marginBottom: '2rem'
      }}>
        <h1 style={{
          fontSize: '2.5rem',
          fontWeight: 'bold',
          color: '#1e40af',
          marginBottom: '0.5rem'
        }}>
          Heidi
        </h1>
        <h2 style={{
          fontSize: '1.25rem',
          color: '#6b7280'
        }}>
          Antibiotic Guide
        </h2>
      </div>

      {/* Main Content */}
      <div style={{
        maxWidth: '1280px',
        margin: '0 auto',
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '2rem',
        height: 'calc(100vh - 200px)'
      }}>
        {/* Left Side - Input Section */}
        <div style={{
          backgroundColor: 'white',
          borderRadius: '0.5rem',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
          padding: '1.5rem',
          display: 'flex',
          flexDirection: 'column'
        }}>
          <label 
            htmlFor="medical-info"
            style={{
              fontSize: '1.125rem',
              fontWeight: '600',
              color: '#374151',
              marginBottom: '1rem'
            }}
          >
            Enter Medical Information
          </label>
          <textarea
            id="medical-info"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Paste your medical information here..."
            style={{
              flex: 1,
              width: '100%',
              padding: '1rem',
              border: '1px solid #d1d5db',
              borderRadius: '0.5rem',
              resize: 'none',
              outline: 'none',
              color: '#374151',
              fontSize: '1rem'
            }}
            onFocus={(e) => {
              e.target.style.borderColor = '#3b82f6'
              e.target.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)'
            }}
            onBlur={(e) => {
              e.target.style.borderColor = '#d1d5db'
              e.target.style.boxShadow = 'none'
            }}
          />
          <button
            onClick={handleSubmit}
            disabled={isLoading}
            style={{
              marginTop: '1rem',
              backgroundColor: isLoading ? '#9ca3af' : '#2563eb',
              color: 'white',
              fontWeight: '600',
              padding: '0.75rem 1.5rem',
              borderRadius: '0.5rem',
              border: 'none',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              fontSize: '1rem',
              transition: 'all 0.2s ease-in-out'
            }}
            onMouseEnter={(e) => {
              if (!isLoading) {
                e.target.style.backgroundColor = '#1d4ed8'
                e.target.style.transform = 'scale(1.05)'
              }
            }}
            onMouseLeave={(e) => {
              if (!isLoading) {
                e.target.style.backgroundColor = '#2563eb'
                e.target.style.transform = 'scale(1)'
              }
            }}
          >
            {isLoading ? 'Sending to Heidi...' : 'Ask Heidi for Antibiotic Guide'}
          </button>
        </div>

        {/* Right Side - Results Section */}
        <div style={{
          backgroundColor: 'white',
          borderRadius: '0.5rem',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
          padding: '1.5rem',
          display: 'flex',
          flexDirection: 'column'
        }}>
          <h3 style={{
            fontSize: '1.125rem',
            fontWeight: '600',
            color: '#374151',
            marginBottom: '1rem'
          }}>
            Heidi Response
          </h3>
          
          {response ? (
            <div style={{
              backgroundColor: '#f9fafb',
              border: '1px solid #e5e7eb',
              borderRadius: '0.5rem',
              padding: '1rem',
              flex: 1,
              whiteSpace: 'pre-wrap',
              color: '#374151',
              fontSize: '0.9rem',
              overflowY: 'auto'
            }}>
              {response}
            </div>
          ) : (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flex: 1,
              color: '#9ca3af',
              textAlign: 'center'
            }}>
              <p style={{ fontSize: '1.125rem' }}>
                {isLoading ? 'Processing your request...' : 'Results will appear here'}
              </p>
            </div>
          )}
        </div>
      </div>
    </main>
  )
}
