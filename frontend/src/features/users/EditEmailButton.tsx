// Archi Savvy Studio ERP - lets an administrator correct a user's sign-in address.
// AGPL-3.0-or-later. New file in this fork; not part of the original project.
import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Check, Mail, Pencil, X } from 'lucide-react';
import { useToastStore } from '@/stores/useToastStore';
import { updateUser, type User } from './api';

/** Built-in accounts are found by their address, so the server refuses to change it. */
const FIXED_ADDRESS = /@(openestimate\.local|openbusinesserp\.com)$/i;
const LOOKS_LIKE_EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function EditableEmail({ user, canEdit }: { user: User; canEdit: boolean }) {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const addToast = useToastStore((s) => s.addToast);
  const [editing, setEditing] = useState(false);
  const [value, setValue] = useState(user.email);

  const save = useMutation({
    mutationFn: (email: string) => updateUser(user.id, { email }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      setEditing(false);
      addToast({
        type: 'success',
        title: t('users.email_updated', { defaultValue: 'Email address updated' }),
        message: t('users.email_updated_hint', {
          defaultValue: 'The user signs in with the new address. The password is unchanged.',
        }),
      });
    },
    onError: (e: Error) => {
      addToast({ type: 'error', title: t('common.error', { defaultValue: 'Error' }), message: e.message });
    },
  });

  const editable = canEdit && !FIXED_ADDRESS.test(user.email);
  const trimmed = value.trim();
  const valid = LOOKS_LIKE_EMAIL.test(trimmed) && trimmed.toLowerCase() !== user.email.toLowerCase();

  if (!editing) {
    return (
      <div className="group flex items-center gap-1.5">
        <Mail size={12} className="text-content-quaternary" />
        <span>{user.email}</span>
        {editable && (
          <button
            type="button"
            onClick={() => {
              setValue(user.email);
              setEditing(true);
            }}
            className="rounded p-1 text-content-quaternary hover:bg-surface-secondary hover:text-content-primary"
            title={t('users.edit_email', { defaultValue: 'Edit email address' })}
            aria-label={t('users.edit_email_for', {
              defaultValue: 'Edit email address of {{name}}',
              name: user.full_name,
            })}
            data-testid={`edit-email-${user.id}`}
          >
            <Pencil size={12} />
          </button>
        )}
      </div>
    );
  }

  const submit = () => {
    if (valid && !save.isPending) save.mutate(trimmed);
  };

  return (
    <div className="flex items-center gap-1.5">
      <input
        type="email"
        autoFocus
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter') submit();
          if (e.key === 'Escape') setEditing(false);
        }}
        className="h-7 w-56 rounded border border-border bg-surface-primary px-2 text-sm text-content-primary focus:border-oe-blue focus:outline-none"
        aria-label={t('users.email', { defaultValue: 'Email' })}
        data-testid={`edit-email-input-${user.id}`}
      />
      <button
        type="button"
        onClick={submit}
        disabled={!valid || save.isPending}
        className="rounded p-1 text-oe-blue hover:bg-surface-secondary disabled:opacity-40"
        title={t('common.save', { defaultValue: 'Save' })}
        aria-label={t('common.save', { defaultValue: 'Save' })}
      >
        <Check size={14} />
      </button>
      <button
        type="button"
        onClick={() => setEditing(false)}
        className="rounded p-1 text-content-tertiary hover:bg-surface-secondary"
        title={t('common.cancel', { defaultValue: 'Cancel' })}
        aria-label={t('common.cancel', { defaultValue: 'Cancel' })}
      >
        <X size={14} />
      </button>
    </div>
  );
}
