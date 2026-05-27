import { useState } from 'react';
import { Heart, Shield, Zap, MessageSquare, ArrowRight, CheckCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const DatingLandingPage = () => {
  const [step, setStep] = useState(0);
  const [answers, setStepAnswers] = useState<string[]>([]);

  const questions = [
    {
      q: "How many matches did you get last week?",
      options: ["0-2", "3-5", "5+", "I stopped counting"]
    },
    {
      q: "What is your biggest frustration?",
      options: ["Ghosting", "Low Quality Matches", "Paying for nothing", "Fake profiles"]
    },
    {
      q: "Have you ever tried a niche dating app?",
      options: ["Yes", "No", "Didn't know they existed"]
    }
  ];

  const handleAnswer = (ans: string) => {
    setStepAnswers([...answers, ans]);
    if (step < questions.length - 1) {
      setStep(step + 1);
    } else {
      setStep(99); // Result state
    }
  };

  return (
    <div className="min-h-screen bg-neutral-50 font-sans text-neutral-900 overflow-x-hidden">
      {/* Navbar */}
      <nav className="fixed top-0 left-0 right-0 bg-white/80 backdrop-blur-md border-b z-50 px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-2 font-bold text-xl text-rose-600">
          <Heart fill="currentColor" />
          <span>MatchFix 2026</span>
        </div>
        <button className="bg-rose-600 text-white px-4 py-2 rounded-full text-sm font-medium hover:bg-rose-700 transition-colors">
          Get the Guide
        </button>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-12 px-6 max-w-4xl mx-auto text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="inline-block px-3 py-1 bg-rose-100 text-rose-700 rounded-full text-xs font-bold mb-6 tracking-wider uppercase"
        >
          Algorithm Workaround 2026
        </motion.div>
        <h1 className="text-4xl md:text-6xl font-black mb-6 leading-tight tracking-tight">
          Stop Swiping Into The <span className="text-rose-600">Void.</span>
        </h1>
        <p className="text-lg text-neutral-600 mb-10 max-w-2xl mx-auto leading-relaxed">
          The big apps are designed to keep you single so you keep paying. Discover the high-intent workflow used by the top 1% of matches.
        </p>
      </section>

      {/* Interactive Audit Quiz */}
      <section className="px-6 mb-24 max-w-2xl mx-auto">
        <div className="bg-white rounded-3xl shadow-xl border border-neutral-100 overflow-hidden">
          <div className="bg-rose-600 px-6 py-3 text-white text-sm font-bold flex justify-between">
            <span>Profile Audit v2.1</span>
            <span>{step < 99 ? `Step ${step + 1}/${questions.length}` : "Analysis Complete"}</span>
          </div>
          
          <div className="p-8 min-h-[350px] flex flex-col justify-center">
            <AnimatePresence mode="wait">
              {step < 99 ? (
                <motion.div
                  key={step}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                >
                  <h2 className="text-2xl font-bold mb-8">{questions[step].q}</h2>
                  <div className="grid gap-4">
                    {questions[step].options.map((opt) => (
                      <button
                        key={opt}
                        onClick={() => handleAnswer(opt)}
                        className="w-full text-left p-4 rounded-xl border-2 border-neutral-100 hover:border-rose-600 hover:bg-rose-50 transition-all font-medium text-neutral-700 group flex justify-between items-center"
                      >
                        {opt}
                        <ArrowRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" />
                      </button>
                    ))}
                  </div>
                </motion.div>
              ) : (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="text-center"
                >
                  <div className="w-16 h-16 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-6">
                    <CheckCircle className="w-10 h-10" />
                  </div>
                  <h2 className="text-2xl font-bold mb-2">Audit Complete!</h2>
                  <p className="text-neutral-500 mb-8 leading-relaxed">
                    Based on your answers, you are currently <span className="text-rose-600 font-bold underline">Shadow-Suppressed</span> by the mainstream algorithm.
                  </p>
                  <a 
                    href="PLACEHOLDER_LINK" 
                    className="block w-full bg-rose-600 text-white font-bold py-4 rounded-xl shadow-lg hover:bg-rose-700 transition-all transform hover:-translate-y-1"
                  >
                    Unlock My 2026 Strategy
                  </a>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="px-6 pb-24 grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
        {[
          { icon: Zap, title: "Pattern Interrupts", desc: "Openers that get a 90% reply rate by breaking the cognitive bias." },
          { icon: Shield, title: "Algorithm Cloaking", desc: "How to stay in the high-priority pool without paying $50/mo." },
          { icon: MessageSquare, title: "Lead Generation", desc: "Switch from swiping to attracting high-intent partners." }
        ].map((f, i) => (
          <div key={i} className="p-6 bg-white rounded-2xl border border-neutral-100 shadow-sm">
            <div className="w-12 h-12 bg-rose-100 text-rose-600 rounded-xl flex items-center justify-center mb-4">
              <f.icon className="w-6 h-6" />
            </div>
            <h3 className="font-bold mb-2">{f.title}</h3>
            <p className="text-sm text-neutral-500 leading-relaxed">{f.desc}</p>
          </div>
        ))}
      </section>

      {/* Footer */}
      <footer className="bg-white border-t py-12 px-6 text-center text-neutral-400 text-sm">
        <p>© 2026 MatchFix Systems. All rights reserved.</p>
        <p className="mt-2 italic">Designed for high-intent, intentional dating.</p>
      </footer>
    </div>
  );
};

export default DatingLandingPage;
