import React, { useState, useRef } from 'react';
import { Camera, UserPlus, X, Check, Trash2, RefreshCw } from 'lucide-react'; import { motion, AnimatePresence } from 'motion/react';
import { EnrolledUser } from '../lib/gemini'; import { cn } from '../lib/utils';

interface EnrollmentProps {
onEnroll: (user: EnrolledUser) => void; enrolledUsers: EnrolledUser[]; onRemove: (id: string) => void;
}


export const Enrollment: React.FC<EnrollmentProps> = ({ onEnroll, enrolledUsers, onRemove }) => {
const [isOpening, setIsOpening] = useState(false); const [name, setName] = useState('');
const [photo, setPhoto] = useState<string | null>(null); const videoRef = useRef<HTMLVideoElement>(null); const canvasRef = useRef<HTMLCanvasElement>(null);

const startCamera = async () => {
 
setIsOpening(true); try {
const stream = await navigator.mediaDevices.getUserMedia({ video: true }); if (videoRef.current) {
videoRef.current.srcObject = stream;
}
} catch (err) { console.error(err); setIsOpening(false);
}
};


const capture = () => {
if (videoRef.current && canvasRef.current) { const canvas = canvasRef.current; canvas.width = videoRef.current.videoWidth; canvas.height = videoRef.current.videoHeight; const ctx = canvas.getContext('2d'); ctx?.drawImage(videoRef.current, 0, 0); setPhoto(canvas.toDataURL('image/jpeg'));

// Stop camera
const stream = videoRef.current.srcObject as MediaStream; stream.getTracks().forEach(track => track.stop());
}
 
};


const handleSubmit = (e: React.FormEvent) => { e.preventDefault();
if (name && photo) { onEnroll({
id: crypto.randomUUID(), name,
photoBase64: photo
});
setName(''); setPhoto(null); setIsOpening(false);
}
};


return (
<div className="space-y-8">
<div className="flex justify-between items-center bg-white p-6 rounded-[32px] border border-blue-50 shadow-sm">
<div>
<h2 className="text-2xl font-black tracking-tight text-slate-800 uppercase">Registry Control</h2>
<p className="text-[10px] font-bold text-blue-500 uppercase tracking-widest mt-1">Authorized Biometric Database</p>
</div>
 
<button
onClick={() => setIsOpening(true)}
className="bg-blue-600 text-white px-6 py-3 rounded-2xl text-xs font-black flex items-center gap-2 hover:bg-blue-700 transition-all shadow-lg shadow-blue-200 uppercase tracking-widest"
>
<UserPlus size={18} /> Enroll Participant
</button>
</div>


<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
<AnimatePresence>
{enrolledUsers.map(user => (
<motion.div key={user.id}
initial={{ opacity: 0, scale: 0.9 }}
animate={{ opacity: 1, scale: 1 }}
exit={{ opacity: 0, scale: 0.9 }}
className="group relative bg-white border border-blue-50 rounded-[32px] overflow-hidden shadow-sm hover:shadow-xl transition-all hover:-translate-y-1"
>
<div className="aspect-[4/5] relative">
<img src={user.photoBase64} alt={user.name} className="w-full h-full object-cover" referrerPolicy="no-referrer" />
<div className="absolute inset-0 bg-gradient-to-t from-slate-900/80 via-
 
transparent to-transparent opacity-60 group-hover:opacity-80 transition-opacity" />
</div>
<div className="p-5 bg-white absolute bottom-0 inset-x-0 flex justify-between items-center border-t border-blue-50">
<div>
<span className="font-black text-sm text-slate-800 tracking-tight block truncate uppercase">{user.name}</span>
<span className="text-[9px] font-bold text-slate-400 uppercase tracking-widest">Enrolled Member</span>
</div>
<button
onClick={() => onRemove(user.id)}
className="p-2 text-rose-500 hover:bg-rose-50 rounded-xl transition-colors opacity-0 group-hover:opacity-100"
title="Remove Member"
>
<Trash2 size={16} />
</button>
</div>
</motion.div>
))}
</AnimatePresence>


{enrolledUsers.length === 0 && (
<div className="col-span-full py-20 border-4 border-dashed border-blue-50 rounded-[44px] flex flex-col items-center justify-center text-slate-300 gap-4 bg-
 
white/50">
<div className="w-20 h-20 bg-blue-50 rounded-full flex items-center justify-center text-blue-200">
<UserPlus size={40} strokeWidth={1} />
</div>
<p className="text-[10px] font-black uppercase tracking-[0.3em]">No participants detected in database</p>
</div>
)}
</div>


<AnimatePresence>
{isOpening && (
<motion.div
initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-md flex items-center justify-center p-4"
>
<motion.div
initial={{ scale: 0.9, opacity: 0, y: 30 }}
animate={{ scale: 1, opacity: 1, y: 0 }}
exit={{ scale: 0.9, opacity: 0, y: 30 }}
className="bg-white rounded-[44px] w-full max-w-xl overflow-hidden relative shadow-2xl border-4 border-white"
 
>
<button
onClick={() => setIsOpening(false)}
className="absolute top-6 right-6 z-10 p-2.5 bg-slate-100 hover:bg-rose-100 hover:text-rose-600 rounded-2xl transition-all"
>
<X size={24} />
</button>


<div className="p-10">
<div className="mb-8">
<h3 className="text-3xl font-black text-slate-800 tracking-tight uppercase">New Enrollment</h3>
<p className="text-[11px] font-bold text-blue-500 uppercase tracking-widest mt-1">Capture biometric reference data</p>
</div>


<form onSubmit={handleSubmit} className="space-y-8">
<div className="aspect-[4/3] bg-slate-900 rounded-[32px] overflow-hidden relative border-4 border-slate-50 shadow-inner">
{!photo ? (
<>
<video ref={videoRef} autoPlay muted className="w-full h-full object-cover opacity-80" />
<div className="absolute inset-0 pointer-events-none border-[3px] border-white/20 m-6 rounded-2xl border-dashed"></div>
 
<button type="button" onClick={capture}
className="absolute bottom-8 left-1/2 -translate-x-1/2 bg-white text-slate-900 px-8 py-3 rounded-2xl font-black shadow-2xl flex items-center gap-3 hover:scale-105 transition-transform uppercase text-xs tracking-widest"
>
<Camera size={20} /> Capture
</button>
{!videoRef.current?.srcObject && (
<div className="absolute inset-0 flex items-center justify-
 
center">
 


<button type="button"
onClick={startCamera}
className="bg-blue-600 text-white px-8 py-4 rounded-2xl font-
 
black uppercase tracking-widest shadow-xl shadow-blue-400/20"
>
Start Sensor
</button>
</div>
)}
</>
) : (
<div className="relative h-full w-full">
 
<img src={photo} className="w-full h-full object-cover" referrerPolicy="no-referrer" />
<div className="absolute inset-0 bg-emerald-500/10 pointer-events-
 
none"></div>
 


<button type="button"
onClick={() => { setPhoto(null); startCamera(); }} className="absolute top-4 right-4 bg-white/90 text-slate-900 p-3
 
rounded-2xl backdrop-blur-md shadow-lg hover:rotate-90 transition-transform"
>
<RefreshCw size={20} />
</button>
</div>
)}
<canvas ref={canvasRef} className="hidden" />
</div>


<div className="space-y-3">
<label className="text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 ml-1">Participant Identity</label>
<input required type="text"
value={name}
onChange={(e) => setName(e.target.value)} placeholder="ENTER FULL NAME"
 
className="w-full bg-slate-50 border-2 border-slate-100 px-6 py-4 rounded-[24px] focus:outline-none focus:border-blue-600 font-black text-slate-800 uppercase text-sm tracking-widest transition-colors"
/>
</div>


<button
disabled={!name || !photo} type="submit"
className="w-full bg-blue-600 text-white py-5 rounded-[24px] font-black disabled:opacity-30 transition-all flex items-center justify-center gap-3 shadow-xl shadow-blue-200 uppercase tracking-widest hover:bg-blue-700"
>
<Check size={24} /> Confirm Database Link
</button>
</form>
</div>
</motion.div>
</motion.div>
)}
</AnimatePresence>
</div>
);
};
