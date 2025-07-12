'use client'

import { useState } from 'react'

export default function Home() {
  const [inputText, setInputText] = useState('')
  const [response, setResponse] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(false)

  const formatHeidiResponse = (data: any) => {
    return (
      <div style={{ 
        color: '#374151', 
        fontSize: '0.95rem', 
        lineHeight: '1.6' 
      }}>
        {/* Status Message */}
        <div style={{
          backgroundColor: '#dcfce7',
          border: '1px solid #bbf7d0',
          borderRadius: '0.5rem',
          padding: '1rem',
          marginBottom: '1.5rem',
          color: '#15803d'
        }}>
          <div style={{ 
            fontWeight: '600', 
            fontSize: '1rem',
            marginBottom: '0.5rem'
          }}>
            ✅ {data.message}
          </div>
        </div>

        {/* Extracted Drugs */}
        <div style={{ marginBottom: '1.5rem' }}>
          <div style={{ 
            fontSize: '1.1rem', 
            fontWeight: '600', 
            color: '#1f2937',
            marginBottom: '0.5rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            💊 <span>Extracted Drugs</span>
          </div>
          <div style={{
            backgroundColor: '#fef3c7',
            border: '1px solid #fcd34d',
            borderRadius: '0.375rem',
            padding: '0.75rem',
            color: '#92400e',
            fontWeight: '500'
          }}>
            {data.extracted_drugs && data.extracted_drugs.length > 0 
              ? data.extracted_drugs.join(', ') 
              : 'None identified'
            }
          </div>
        </div>

        {/* Vector Context */}
        {data.vector_context && data.vector_context.length > 0 && (
          <div style={{ marginBottom: '1.5rem' }}>
            <div style={{ 
              fontSize: '1.1rem', 
              fontWeight: '600', 
              color: '#1f2937',
              marginBottom: '0.5rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}>
              📚 <span>Reference Database</span>
            </div>
            <div style={{
              backgroundColor: '#e0e7ff',
              border: '1px solid #c7d2fe',
              borderRadius: '0.375rem',
              padding: '0.75rem',
              color: '#3730a3',
              fontWeight: '500'
            }}>
              Found {data.vector_context.length} relevant reference chunks
            </div>
          </div>
        )}

        {/* Clinical Summary */}
        {data.final_summary && (
          <div style={{ marginBottom: '1.5rem' }}>
            <div style={{ 
              fontSize: '1.1rem', 
              fontWeight: '600', 
              color: '#1f2937',
              marginBottom: '0.75rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}>
              🧠 <span>Heidi's Clinical Summary</span>
            </div>
            <div style={{
              backgroundColor: '#f0f9ff',
              border: '1px solid #bae6fd',
              borderRadius: '0.5rem',
              padding: '1.25rem',
              color: '#0c4a6e',
              whiteSpace: 'pre-wrap',
              lineHeight: '1.7'
            }}>
              {data.final_summary}
            </div>
            <div style={{
              marginTop: '0.75rem',
              padding: '0.75rem',
              backgroundColor: '#fef2f2',
              border: '1px solid #fecaca',
              borderRadius: '0.375rem',
              fontSize: '0.875rem',
              color: '#991b1b',
              fontStyle: 'italic',
              textAlign: 'center'
            }}>
              ⚠️ This information may not be up to date and does not constitute medical advice, diagnosis, or treatment recommendations.
            </div>
          </div>
        )}

        {/* Processing Steps */}
        {data.processing_steps && data.processing_steps.length > 0 && (
          <div>
            <div style={{ 
              fontSize: '1.1rem', 
              fontWeight: '600', 
              color: '#1f2937',
              marginBottom: '0.75rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}>
              ⚙️ <span>Processing Steps</span>
            </div>
            <div style={{
              backgroundColor: '#f8fafc',
              border: '1px solid #e2e8f0',
              borderRadius: '0.5rem',
              padding: '1rem'
            }}>
              {data.processing_steps.map((step: string, index: number) => (
                <div key={index} style={{
                  padding: '0.5rem 0',
                  borderBottom: index < data.processing_steps.length - 1 ? '1px solid #e2e8f0' : 'none',
                  color: '#475569',
                  fontSize: '0.9rem'
                }}>
                  <span style={{ 
                    fontWeight: '600', 
                    color: '#334155',
                    marginRight: '0.5rem' 
                  }}>
                    {index + 1}.
                  </span>
                  {step}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    )
  }

  const handleSubmit = async () => {
    if (!inputText.trim()) {
      alert('Please enter some medical information first.')
      return
    }

    setIsLoading(true)
    setResponse(null)

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
      
      // Store the response data for formatting
      setResponse(data)
      console.log('Backend response:', data)
      
    } catch (error) {
      console.error('Error calling backend:', error)
      setResponse({ message: 'Error: Failed to connect to backend API', error: true })
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
              width: 'calc(100% - 2rem)',
              maxWidth: '100%',
              padding: '1rem',
              border: '1px solid #d1d5db',
              borderRadius: '0.5rem',
              resize: 'none',
              outline: 'none',
              color: '#374151',
              fontSize: '1rem',
              boxSizing: 'border-box'
            }}
            onFocus={(e) => {
              (e.target as HTMLTextAreaElement).style.borderColor = '#3b82f6';
              (e.target as HTMLTextAreaElement).style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)'
            }}
            onBlur={(e) => {
              (e.target as HTMLTextAreaElement).style.borderColor = '#d1d5db';
              (e.target as HTMLTextAreaElement).style.boxShadow = 'none'
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
                (e.target as HTMLButtonElement).style.backgroundColor = '#1d4ed8';
                (e.target as HTMLButtonElement).style.transform = 'scale(1.05)'
              }
            }}
            onMouseLeave={(e) => {
              if (!isLoading) {
                (e.target as HTMLButtonElement).style.backgroundColor = '#2563eb';
                (e.target as HTMLButtonElement).style.transform = 'scale(1)'
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
              flex: 1,
              overflowY: 'auto'
            }}>
              {formatHeidiResponse(response)}
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
