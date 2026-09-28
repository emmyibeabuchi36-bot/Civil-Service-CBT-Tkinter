import tkinter as tk
from tkinter import ttk, messagebox
from .auth import AuthenticationService
from .admin import AdminService

class CBTApplication(tk.Tk):
    def __init__(self, db, auth, bank, exam, results, admin):
        super().__init__(); self.title("FCT Civil Service Promotion CBT"); self.geometry("900x650"); self.minsize(820,600)
        self.db,self.auth,self.bank,self.exam,self.results,self.admin=db,auth,bank,exam,results,admin
        self.user=None; self.questions=[]; self.answers={}; self.index=0; self.remaining=0; self.timer_id=None; self.show_login()
    def clear(self):
        for w in self.winfo_children(): w.destroy()
    def header(self, title): ttk.Label(self,text=title,font=("Segoe UI",22,"bold")).pack(pady=25)
    def show_login(self):
        self.clear(); self.header("FCT Civil Service Promotion CBT")
        f=ttk.Frame(self,padding=25); f.pack()
        self.login_user=tk.StringVar(); self.login_pass=tk.StringVar()
        ttk.Label(f,text="Username").grid(row=0,column=0,pady=8,sticky="w"); ttk.Entry(f,textvariable=self.login_user,width=35).grid(row=0,column=1)
        ttk.Label(f,text="Password").grid(row=1,column=0,pady=8,sticky="w"); ttk.Entry(f,textvariable=self.login_pass,show="*",width=35).grid(row=1,column=1)
        ttk.Button(f,text="Login",command=self.do_login).grid(row=2,column=0,columnspan=2,pady=15)
        ttk.Button(f,text="Register Candidate",command=self.show_register).grid(row=3,column=0,columnspan=2)
        ttk.Label(self,text="Demo: candidate/candidate123  |  admin/admin123").pack(pady=20)
    def do_login(self):
        self.user=self.auth.login(self.login_user.get(),self.login_pass.get())
        if not self.user: messagebox.showerror("Login","Invalid username or password."); return
        self.show_dashboard()
    def show_register(self):
        self.clear(); self.header("Candidate Registration")
        f=ttk.Frame(self,padding=20); f.pack(); vars=[tk.StringVar() for _ in range(3)]
        for i,(label,var) in enumerate(zip(["Full name","Username","Password"],vars)):
            ttk.Label(f,text=label).grid(row=i,column=0,pady=8,sticky="w"); ttk.Entry(f,textvariable=var,show="*" if i==2 else "",width=35).grid(row=i,column=1)
        def register():
            ok,msg=self.auth.register(*[v.get() for v in vars]); messagebox.showinfo("Registration",msg) if ok else messagebox.showerror("Registration",msg)
            if ok:self.show_login()
        ttk.Button(f,text="Create Account",command=register).grid(row=3,column=0,columnspan=2,pady=15); ttk.Button(f,text="Back",command=self.show_login).grid(row=4,column=0,columnspan=2)
    def show_dashboard(self):
        self.clear(); self.header(f"Welcome, {self.user.full_name}")
        f=ttk.Frame(self,padding=20); f.pack()
        if self.user.role=="admin": ttk.Button(f,text="Admin Question Management",command=self.show_admin).pack(fill="x",pady=7)
        else:
            ttk.Button(f,text="Start CBT Examination",command=self.start_exam).pack(fill="x",pady=7)
            ttk.Button(f,text="View Result History",command=self.show_history).pack(fill="x",pady=7)
        ttk.Button(f,text="Logout",command=self.logout).pack(fill="x",pady=20)
    def logout(self): self.user=None; self.cancel_timer(); self.show_login()
    def start_exam(self):
        self.questions,self.attempt_id=self.exam.create_exam(self.user); self.answers={}; self.index=0; self.remaining=self.exam.DURATION_SECONDS; self.show_exam(); self.tick()
    def show_exam(self):
        self.clear(); q=self.questions[self.index]
        top=ttk.Frame(self); top.pack(fill="x",padx=25,pady=15); ttk.Label(top,text=f"Question {self.index+1} of {len(self.questions)}",font=("Segoe UI",14,"bold")).pack(side="left"); self.timer_label=ttk.Label(top,text="",font=("Segoe UI",14,"bold")); self.timer_label.pack(side="right")
        ttk.Label(self,text=q.question_text,font=("Segoe UI",16,"bold"),wraplength=780).pack(pady=30,padx=30)
        self.choice=tk.StringVar(value=self.answers.get(q.id,"")); f=ttk.Frame(self); f.pack(anchor="w",padx=90)
        for letter,text in zip("ABCD",[q.option_a,q.option_b,q.option_c,q.option_d]): ttk.Radiobutton(f,text=f"{letter}. {text}",variable=self.choice,value=letter).pack(anchor="w",pady=8)
        nav=ttk.Frame(self); nav.pack(pady=30)
        ttk.Button(nav,text="Previous",command=self.previous,state="normal" if self.index else "disabled").pack(side="left",padx=5)
        ttk.Button(nav,text="Next",command=self.next,state="normal" if self.index<len(self.questions)-1 else "disabled").pack(side="left",padx=5)
        ttk.Button(nav,text="Submit Exam",command=self.submit_exam).pack(side="left",padx=5)
    def save_choice(self):
        self.answers[self.questions[self.index].id]=self.choice.get()
    def previous(self): self.save_choice(); self.index-=1; self.show_exam()
    def next(self): self.save_choice(); self.index+=1; self.show_exam()
    def submit_exam(self):
        self.save_choice(); self.cancel_timer(); result=self.exam.grade(self.user,self.questions,self.answers,self.attempt_id); self.show_result(result)
    def show_result(self,r):
        self.clear(); self.header("Examination Result"); ttk.Label(self,text=f"Score: {r.score}/{r.total}\nPercentage: {r.percentage}%\nGrade: {r.grade}\nStatus: {'PASSED' if r.passed else 'FAILED'}",font=("Segoe UI",18,"bold"),justify="center").pack(pady=40); ttk.Button(self,text="Back to Dashboard",command=self.show_dashboard).pack()
    def show_history(self):
        self.clear(); self.header("Result History"); tree=ttk.Treeview(self,columns=("score","percent","grade","status","date"),show="headings")
        for c,t in zip(tree["columns"],["Score","Percentage","Grade","Status","Date"]): tree.heading(c,text=t)
        for r in self.results.history(self.user.id): tree.insert("", "end", values=(f"{r['score']}/{r['total']}",f"{r['percentage']}%",r['grade'],"PASS" if r['passed'] else "FAIL",r['taken_at']))
        tree.pack(fill="both",expand=True,padx=30,pady=10); ttk.Button(self,text="Back",command=self.show_dashboard).pack(pady=10)
    def show_admin(self):
        self.clear(); self.header("Administrator — Question Management")
        outer=ttk.Frame(self,padding=15); outer.pack(fill="both",expand=True)
        vars=[tk.StringVar() for _ in range(7)]; labels=["Question","Option A","Option B","Option C","Option D","Correct (A-D)","Category"]
        for i,(label,var) in enumerate(zip(labels,vars)):
            ttk.Label(outer,text=label).grid(row=i,column=0,pady=3,sticky="w"); ttk.Entry(outer,textvariable=var,width=65).grid(row=i,column=1,pady=3)
        def add():
            try:self.admin.add_question(*[v.get() for v in vars]); messagebox.showinfo("Admin","Question added."); self.show_admin()
            except ValueError as e: messagebox.showerror("Admin",str(e))
        ttk.Button(outer,text="Add Question",command=add).grid(row=7,column=0,columnspan=2,pady=10)
        tree=ttk.Treeview(outer,columns=("id","question","category"),show="headings",height=9); [tree.heading(c,text=t) for c,t in zip(tree["columns"],["ID","Question","Category"])];
        for q in self.bank.all(): tree.insert("", "end", values=(q.id,q.question_text,q.category))
        tree.grid(row=8,column=0,columnspan=2,sticky="nsew"); outer.rowconfigure(8,weight=1); outer.columnconfigure(1,weight=1)
        def delete():
            sel=tree.selection()
            if not sel:return
            qid=int(tree.item(sel[0],"values")[0]); self.admin.delete_question(qid); self.show_admin()
        ttk.Button(outer,text="Delete Selected",command=delete).grid(row=9,column=0,pady=8); ttk.Button(outer,text="Back",command=self.show_dashboard).grid(row=9,column=1,pady=8)
    def tick(self):
        if self.remaining<=0: self.submit_exam(); return
        m,s=divmod(self.remaining,60); self.timer_label.config(text=f"Time: {m:02d}:{s:02d}"); self.remaining-=1; self.timer_id=self.after(1000,self.tick)
    def cancel_timer(self):
        if self.timer_id: self.after_cancel(self.timer_id); self.timer_id=None
