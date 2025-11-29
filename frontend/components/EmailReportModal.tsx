"use client";

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Mail, Send, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';

interface EmailReportModalProps {
  isOpen: boolean;
  onClose: () => void;
  analysisId: string;
  tokenSymbol: string;
  tokenName: string;
}

interface EmailFormData {
  toEmail: string;
  ccEmails: string;
}

export default function EmailReportModal({
  isOpen,
  onClose,
  analysisId,
  tokenSymbol,
  tokenName
}: EmailReportModalProps) {
  const [formData, setFormData] = useState<EmailFormData>({
    toEmail: '',
    ccEmails: ''
  });
  
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setStatus('idle');
    setMessage('');

    try {
      // Parse CC emails (comma-separated)
      const ccArray = formData.ccEmails
        .split(',')
        .map(email => email.trim())
        .filter(email => email.length > 0);

      const response = await fetch('http://localhost:8000/api/send-email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          to_email: formData.toEmail,
          analysis_id: analysisId,
          cc: ccArray
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to send email');
      }

      setStatus('success');
      setMessage(data.message || 'Email sent successfully! Check your inbox.');
      
      // Close modal after 2 seconds on success
      setTimeout(() => {
        onClose();
        setFormData({ toEmail: '', ccEmails: '' });
        setStatus('idle');
      }, 2000);

    } catch (error: any) {
      setStatus('error');
      setMessage(error.message || 'Failed to send email. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          >
            {/* Modal */}
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              transition={{ type: 'spring', damping: 25, stiffness: 300 }}
              className="bg-white w-full max-w-md rounded-2xl shadow-2xl flex flex-col max-h-[90vh] relative"
              onClick={(e) => e.stopPropagation()}
            >
              {/* Header */}
              <div className="bg-blue-600 px-6 py-4 text-white relative flex-shrink-0 rounded-t-2xl">
                <button
                  onClick={onClose}
                  className="absolute right-4 top-4 text-white/80 hover:text-white transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
                
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-white/20 rounded-lg">
                    <Mail className="w-6 h-6" />
                  </div>
                  <div>
                    <h2 className="text-lg font-bold">Email Analysis Report</h2>
                    <p className="text-xs text-white/90 mt-0.5">
                      {tokenSymbol} - {tokenName}
                    </p>
                  </div>
                </div>
              </div>

              {/* Scrollable Body */}
              <div className="overflow-y-auto p-6 flex-1">
                <form id="email-form" onSubmit={handleSubmit} className="space-y-4">
                  {/* To Email */}
                  <div>
                    <label 
                      htmlFor="toEmail" 
                      className="block text-sm font-medium text-gray-700 mb-1.5"
                    >
                      Recipient Email *
                    </label>
                    <input
                      type="email"
                      id="toEmail"
                      name="toEmail"
                      value={formData.toEmail}
                      onChange={handleInputChange}
                      required
                      placeholder="recipient@example.com"
                      className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    />
                  </div>

                  {/* CC Emails */}
                  <div>
                    <label 
                      htmlFor="ccEmails" 
                      className="block text-sm font-medium text-gray-700 mb-1.5"
                    >
                      CC (Optional)
                    </label>
                    <input
                      type="text"
                      id="ccEmails"
                      name="ccEmails"
                      value={formData.ccEmails}
                      onChange={handleInputChange}
                      placeholder="email1@example.com, email2@example.com"
                      className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      Separate multiple emails with commas
                    </p>
                  </div>

                  {/* Info Box */}
                  <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-xl p-6 shadow-sm">
                    <div className="flex gap-4">
                      <div className="flex-shrink-0 mt-1">
                        <div className="p-3 bg-blue-500 rounded-xl">
                          <Mail className="w-6 h-6 text-white" />
                        </div>
                      </div>
                      <div>
                        <p className="font-bold text-blue-900 mb-4 text-lg">What will be sent:</p>
                        <ul className="space-y-3">
                          <li className="flex items-start gap-3 text-base text-gray-800">
                            <span className="text-blue-600 font-bold text-xl leading-none mt-0.5">•</span>
                            <span className="font-medium">Professional analysis report (PDF)</span>
                          </li>
                          <li className="flex items-start gap-3 text-base text-gray-800">
                            <span className="text-blue-600 font-bold text-xl leading-none mt-0.5">•</span>
                            <span className="font-medium">Readiness score & grade</span>
                          </li>
                          <li className="flex items-start gap-3 text-base text-gray-800">
                            <span className="text-blue-600 font-bold text-xl leading-none mt-0.5">•</span>
                            <span className="font-medium">Exchange recommendations</span>
                          </li>
                          <li className="flex items-start gap-3 text-base text-gray-800">
                            <span className="text-blue-600 font-bold text-xl leading-none mt-0.5">•</span>
                            <span className="font-medium">Actionable next steps</span>
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>

                  {/* Status Messages */}
                  <AnimatePresence mode="wait">
                    {status !== 'idle' && (
                      <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className={`flex items-center gap-3 p-3 rounded-lg ${
                          status === 'success' 
                            ? 'bg-green-50 border border-green-200 text-green-800' 
                            : 'bg-red-50 border border-red-200 text-red-800'
                        }`}
                      >
                        {status === 'success' ? (
                          <CheckCircle className="w-5 h-5 flex-shrink-0" />
                        ) : (
                          <AlertCircle className="w-5 h-5 flex-shrink-0" />
                        )}
                        <p className="text-sm font-medium">{message}</p>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </form>
              </div>

              {/* Fixed Footer */}
              <div className="p-4 border-t border-gray-100 bg-gray-50 rounded-b-2xl flex-shrink-0">
                <div className="flex gap-3">
                  <button
                    type="button"
                    onClick={onClose}
                    disabled={isLoading}
                    className="flex-1 px-4 py-2.5 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium text-sm"
                  >
                    Cancel
                  </button>
                  
                  <button
                    type="submit"
                    form="email-form"
                    disabled={isLoading || !formData.toEmail}
                    className="flex-1 px-4 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed font-medium flex items-center justify-center gap-2 shadow-sm text-sm"
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        Sending...
                      </>
                    ) : (
                      <>
                        <Send className="w-4 h-4" />
                        Send Email
                      </>
                    )}
                  </button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}