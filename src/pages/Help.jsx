import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button, Input, PageHeader } from '../components';
import { mockFAQs } from '../data';

export default function Help() {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [expandedId, setExpandedId] = useState(null);
  const [activeCategory, setActiveCategory] = useState(null);

  const filteredFAQs = mockFAQs.filter(faq => {
    const matchesSearch = !searchTerm ||
      faq.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
      faq.answer.toLowerCase().includes(searchTerm.toLowerCase()) ||
      faq.category.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = !activeCategory || faq.category === activeCategory;
    return matchesSearch && matchesCategory;
  });

  const categories = [...new Set(mockFAQs.map(faq => faq.category))];

  return (
    <div className="min-h-screen bg-noise-grid">
      <PageHeader title="Help & Support" onBack={() => navigate(-1)} />

      <motion.div
        className="max-w-4xl mx-auto px-4 sm:px-6 py-12"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* Search */}
        <div className="mb-8">
          <Input
            type="text"
            placeholder="Search FAQs..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full"
          />
        </div>

        {/* Quick Actions */}
        <div className="grid md:grid-cols-3 gap-4 mb-12">
          {[
            { icon: '💬', title: 'Contact Support', sub: 'Chat with our team' },
            { icon: '📧', title: 'Email Us', sub: 'support@satscardapp.com' },
            { icon: '📱', title: 'Call Us', sub: '+1-800-SATSCARD' },
          ].map(action => (
            <motion.button
              key={action.title}
              whileHover={{ y: -4 }}
              className="panel p-6 hover:border-amber/30 transition-all text-left"
            >
              <div className="text-3xl mb-3">{action.icon}</div>
              <p className="font-semibold text-ink mb-1">{action.title}</p>
              <p className="text-sm text-ink-soft">{action.sub}</p>
            </motion.button>
          ))}
        </div>

        {/* Categories */}
        <div className="mb-8">
          <h2 className="heading-3 mb-4">Browse by Category</h2>
          <div className="flex flex-wrap gap-2">
            {categories.map(category => (
              <button
                key={category}
                onClick={() => setActiveCategory(activeCategory === category ? null : category)}
                className={`px-4 py-2 rounded-xl font-medium text-sm transition-all ${
                  activeCategory === category
                    ? 'bg-amber-lime text-bg'
                    : 'bg-elevated hover:bg-white/10 border border-line text-ink'
                }`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        {/* FAQs */}
        <div className="space-y-3">
          <h2 className="heading-3 mb-6">
            Frequently Asked Questions
            {searchTerm && <span className="text-ink-muted font-normal text-lg ml-2">({filteredFAQs.length})</span>}
          </h2>

          {filteredFAQs.length > 0 ? (
            filteredFAQs.map((faq, index) => (
              <motion.div
                key={faq.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.04 }}
              >
                <button
                  onClick={() => setExpandedId(expandedId === faq.id ? null : faq.id)}
                  className="w-full panel p-6 hover:border-amber/30 transition-all text-left group"
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <p className="font-semibold text-ink group-hover:text-amber transition-colors">
                        {faq.question}
                      </p>
                      <p className="text-xs text-ink-muted mt-2">{faq.category}</p>
                    </div>
                    <span className={`text-lg text-ink-muted transition-transform ml-4 ${expandedId === faq.id ? 'rotate-180' : ''}`}>
                      ▼
                    </span>
                  </div>

                  {expandedId === faq.id && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="mt-4 pt-4 border-t border-line"
                    >
                      <p className="text-ink-soft leading-relaxed">{faq.answer}</p>
                    </motion.div>
                  )}
                </button>
              </motion.div>
            ))
          ) : (
            <div className="panel p-12 text-center">
              <p className="text-ink text-lg">No FAQs found</p>
              <p className="text-ink-muted text-sm mt-2">Try a different search term</p>
            </div>
          )}
        </div>

        {/* Contact Form */}
        <div className="mt-12 panel p-8">
          <h2 className="heading-3 mb-6">Can't find an answer?</h2>
          <p className="text-ink-soft mb-6">
            Fill out the form below and our support team will get back to you within 24 hours.
          </p>

          <form className="space-y-4">
            <Input label="Name" type="text" placeholder="Your name" />
            <Input label="Email" type="email" placeholder="your@email.com" />

            <div>
              <label className="text-xs font-semibold text-ink-muted block mb-2 uppercase tracking-wider">Message</label>
              <textarea
                className="w-full px-4 py-3 bg-surface border border-line rounded-xl text-ink resize-none focus:outline-none"
                rows="6"
                placeholder="Describe your issue..."
              />
            </div>

            <Button className="w-full" size="lg">
              Send Message
            </Button>
          </form>
        </div>

        {/* Knowledge Base */}
        <div className="mt-12 panel-elevated p-8 border-amber/20">
          <h2 className="heading-3 mb-4">Documentation</h2>
          <p className="text-ink-soft mb-6">
            Explore our comprehensive knowledge base for detailed guides and tutorials.
          </p>
          <div className="grid md:grid-cols-2 gap-4">
            <a href="#" className="text-amber hover:brightness-110 font-semibold">📚 Getting Started Guide</a>
            <a href="#" className="text-amber hover:brightness-110 font-semibold">⚡ Lightning Network Guide</a>
            <a href="#" className="text-amber hover:brightness-110 font-semibold">🔒 Security Best Practices</a>
            <a href="#" className="text-amber hover:brightness-110 font-semibold">💰 Managing Your Balance</a>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
