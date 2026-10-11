/-
∗21.  General Theory of Relations.

Formalization of chapter ∗21 ("General Theory of Relations"), Section C,
Part I of Whitehead & Russell's *Principia Mathematica* (Volume I).
This chapter introduces the general theory of dyadic relations, paralleling
chapter ∗20 for classes, which forms the foundation for relation-arithmetic,
ordinal arithmetic, and series in Volumes II and III.

Modelling decision (recorded for faithfulness review):
------------------------------------------------------
*Principia* introduces relations by the "no-relations" device ∗21·01:

    f{x̂ŷ(ψ(x, y))} . =: (∃φ): φ!(x, y) .≡_{x, y}. ψ(x, y) : f{φ!x̂ŷ}   Df

i.e. a statement about a relation is, by definition, an extensional
statement about its defining two-variable propositional function.
The central theorems of ∗21 (∗21·15, ∗21·31, ∗21·43) establish that this
device behaves exactly like an extensional notion of relation: two relations
are identical iff their defining functions are formally equivalent iff they
hold for the same pairs.

In an extensional type theory (Lean 4), this extensionality is directly available:
  * relation between individuals of type `α` and `β` ↦ `Rel α β := Set (α × β)`
  * relation abstraction `x̂ŷ(ψ(x, y))`              ↦ `relOf ψ := { p : α × β | ψ p.1 p.2 }`
  * relation application `x R y`                     ↦ `(x, y) ∈ R`
  * relation identity `R = S`                        ↦ set equality `R = S`
  * non-relation `x ~R y`                            ↦ `(x, y) ∉ R` (∗21·06)

Metatheoretic items NOT rendered as object-level theorems:
---------------------------------------------------------
The ramified-type / axiom-of-reducibility bookkeeping propositions for relations —
∗21·01 (defining convention), ∗21·03 (definition of `Rel`), ∗21·07–∗21·081
(notational conventions), and the predicative-function lemmas ∗21·1, ∗21·11,
∗21·111, ∗21·12, ∗21·151 (asserting that every relation arises from a predicative
function) — are absorbed into this extensional model and recorded as commentary,
matching the policy established in ∗20 (`Classes.lean`).

The genuine mathematical theorems of the chapter (∗21·15 through ∗21·43)
are formalized below with 0 sorry and 0 custom axioms.
-/

import Mathlib

namespace Principia.Part1.Section3

variable {α β : Type*}

/-- Binary relation between individuals of type `α` and `β`. -/
abbrev Rel (α β : Type*) := Set (α × β)

/-- Relation abstraction x̂ŷ(ψ(x, y)): the relation determined by predicate `P`. -/
def relOf (P : α → β → Prop) : Rel α β := { p | P p.1 p.2 }

/-! ### Definitions (∗21·02–∗21·06) -/

-- ∗21·02  x {x̂ŷ(φ(x, y))} y .≡. φ(x, y)
theorem ast_21_02 (x : α) (y : β) (P : α → β → Prop) :
    ((x, y) ∈ relOf P) ↔ P x y := Iff.rfl

-- ∗21·06  x ~R y .=. ¬(x R y)  Df
theorem ast_21_06 (x : α) (y : β) (R : Rel α β) :
    ((x, y) ∉ R) ↔ ¬ ((x, y) ∈ R) := Iff.rfl

/-! ### Fundamental properties of relations (∗21·15–∗21·25) -/

-- ∗21·15  ⊢ :. ψ(x, y) .≡_{x,y}. χ(x, y) : ≡ . x̂ŷ(ψ(x, y)) = x̂ŷ(χ(x, y))
-- "Two functions determine the same relation when, and only when, they are
-- formally equivalent." (Fundamental extensionality theorem of ∗21).
theorem ast_21_15 (P Q : α → β → Prop) :
    (∀ x y, P x y ↔ Q x y) ↔ (relOf P = relOf Q) := by
  constructor
  · intro h
    ext ⟨x, y⟩
    exact h x y
  · intro h x y
    have := congr_arg (fun s : Rel α β => (x, y) ∈ s) h
    simpa [relOf] using this

-- ∗21·18  ⊢ :. x̂ŷ(φ(x, y)) = x̂ŷ(ψ(x, y)) .⊃: f{x̂ŷ(φ(x, y))} ≡ f{x̂ŷ(ψ(x, y))}
theorem ast_21_18 (P Q : α → β → Prop) (f : Rel α β → Prop) :
    relOf P = relOf Q → (f (relOf P) ↔ f (relOf Q)) := by
  rintro h; rw [h]

-- ∗21·191 ⊢ :. x̂ŷ(φ(x, y)) = x̂ŷ(χ(x, y)) .≡: (f) : f!x̂ŷ(φ(x, y)) .≡. f!x̂ŷ(χ(x, y))
-- (Leibniz characterization of relation identity)
theorem ast_21_191 (P Q : α → β → Prop) :
    (relOf P = relOf Q) ↔ ∀ f : Rel α β → Prop, f (relOf P) ↔ f (relOf Q) := by
  constructor
  · rintro h f; rw [h]
  · intro h; exact (h (fun s => relOf P = s)).mp rfl

-- ∗21·2  ⊢ . x̂ŷ(φ(x, y)) = x̂ŷ(φ(x, y))  (Reflexivity of relation identity)
theorem ast_21_2 (P : α → β → Prop) : relOf P = relOf P := rfl

-- ∗21·21  ⊢ : R = S .≡. S = R  (Symmetry of relation identity)
theorem ast_21_21 (R S : Rel α β) : (R = S) ↔ (S = R) := eq_comm

-- ∗21·22  ⊢ : R = S . S = T .⊃. R = T  (Transitivity of relation identity)
theorem ast_21_22 (R S T : Rel α β) : R = S → S = T → R = T := fun h₁ h₂ => h₁.trans h₂

-- ∗21·23  ⊢ : R = S . R = T .⊃. S = T
theorem ast_21_23 (R S T : Rel α β) : R = S → R = T → S = T := fun h₁ h₂ => h₁.symm.trans h₂

-- ∗21·24  ⊢ : S = R . T = R .⊃. S = T
theorem ast_21_24 (R S T : Rel α β) : S = R → T = R → S = T := fun h₁ h₂ => h₁.trans h₂.symm

-- ∗21·25  ⊢ :. R = x̂ŷ(φ(x, y)) .≡_{R}. R = x̂ŷ(ψ(x, y)) : ≡ . x̂ŷ(φ(x, y)) = x̂ŷ(ψ(x, y))
theorem ast_21_25 (P Q : α → β → Prop) :
    (∀ R : Rel α β, (R = relOf P) ↔ (R = relOf Q)) ↔ (relOf P = relOf Q) := by
  constructor
  · intro h; exact (h (relOf P)).mp rfl
  · rintro h R; rw [h]

/-! ### Application, extensionality and relations in-use (∗21·3–∗21·43) -/

-- ∗21·3  ⊢ :. x {x̂ŷ(φ(x, y))} y .≡. φ(x, y)
theorem ast_21_3 (x : α) (y : β) (P : α → β → Prop) :
    ((x, y) ∈ relOf P) ↔ P x y := Iff.rfl

-- ∗21·31  ⊢ :. R = x̂ŷ(φ(x, y)) .≡: x R y .≡_{x, y}. φ(x, y)
theorem ast_21_31 (R : Rel α β) (P : α → β → Prop) :
    (R = relOf P) ↔ (∀ x y, ((x, y) ∈ R) ↔ P x y) := by
  constructor
  · rintro rfl x y; rfl
  · intro h
    ext ⟨x, y⟩
    exact h x y

-- ∗21·32  ⊢ :. R = S .≡: x R y .≡_{x, y}. x S y
theorem ast_21_32 (R S : Rel α β) :
    (R = S) ↔ (∀ x y, ((x, y) ∈ R) ↔ ((x, y) ∈ S)) := by
  constructor
  · rintro rfl x y; rfl
  · intro h
    ext ⟨x, y⟩
    exact h x y

-- ∗21·34  ⊢ :. R = S .⊃: x R y .≡. x S y
theorem ast_21_34 (R S : Rel α β) (x : α) (y : β) :
    R = S → (((x, y) ∈ R) ↔ ((x, y) ∈ S)) := by
  rintro rfl; rfl

-- ∗21·35  ⊢ :. x̂ŷ(φ(x, y)) = x̂ŷ(ψ(x, y)) .⊃: φ(x, y) .≡. ψ(x, y)
theorem ast_21_35 (P Q : α → β → Prop) (x : α) (y : β) :
    relOf P = relOf Q → (P x y ↔ Q x y) := by
  intro h
  have := ast_21_15 P Q
  exact (this.mpr h) x y

-- ∗21·4  ⊢ :. R = S .≡: (p : α × β): p ∈ R .≡. p ∈ S
theorem ast_21_4 (R S : Rel α β) :
    (R = S) ↔ ∀ p : α × β, (p ∈ R) ↔ (p ∈ S) := Set.ext_iff

-- ∗21·42  ⊢ . R = x̂ŷ(x R y)  (Every relation is the relation abstracted from its application)
theorem ast_21_42 (R : Rel α β) : R = relOf (fun x y => (x, y) ∈ R) := by
  ext ⟨x, y⟩; rfl

-- ∗21·43  ⊢ :. R = S .≡: (x, y): x R y .≡. x S y
theorem ast_21_43 (R S : Rel α β) :
    (R = S) ↔ (∀ x y, ((x, y) ∈ R) ↔ ((x, y) ∈ S)) := ast_21_32 R S

end Principia.Part1.Section3
